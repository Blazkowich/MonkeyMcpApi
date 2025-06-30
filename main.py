import asyncio
import json
import logging

from flask import Flask, request
from flask_restx import Api, Resource, fields

from Agents.GeminiClient import GeminiClient
from Agents.McpServer import McpServer
from Globals.Constants import Monkeys_Url, available_fields, Swagger_Version, Swagger_Title, Swagger_Description, \
    Swagger_Doc, Swagger_Prefix, CHAT_NS
from Helpers.ExtractQueryInfo import extract_query_info
from Helpers.WordCorrection import correct_typos_with_gemini
from Services.MonkeyService import MonkeyService
from Services.MonkeyServiceOptions import MonkeyServiceOptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    monkey_service_options = MonkeyServiceOptions(api_url=Monkeys_Url)

    monkey_service = MonkeyService(monkey_service_options)
    mcp_server = McpServer(monkey_service)
    gemini_client = GeminiClient()

    application = Flask(__name__)

    api = Api(
        application,
        version=Swagger_Version,
        title=Swagger_Title,
        description=Swagger_Description,
        doc=Swagger_Doc,
        prefix=Swagger_Prefix
    )

    api.add_namespace(CHAT_NS, path='/chat')

    error_model = api.model('Error', {
        'error': fields.String(required=True, description='Error message')
    })

    chat_request = api.model('ChatRequest', {
        'message': fields.String(required=True, description='User message for chat')
    })

    chat_response = api.model('ChatResponse', {
        'response': fields.Raw(description='Chat response (can be text or JSON)')
    })

    @CHAT_NS.route('/')
    class Chat(Resource):
        @CHAT_NS.expect(chat_request)
        @CHAT_NS.marshal_with(chat_response)
        @CHAT_NS.response(400, 'Bad Request', error_model)
        @CHAT_NS.response(500, 'Internal Server Error', error_model)
        def post(self):
            data = request.get_json()
            user_input = data.get("message", "")

            if not user_input:
                api.abort(400, "Message is required")

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            try:
                query_info = loop.run_until_complete(extract_query_info(user_input, gemini_client))
                tool_name = query_info.get("tool_name")
                arguments = query_info.get("arguments", {})

                if tool_name == "chat" and arguments.get("message") == "Request Is Out Of Context":
                    return {"response": "Request Is Out Of Context"}

                possible_fields = list(arguments.keys())
                corrected_fields = loop.run_until_complete(
                    correct_typos_with_gemini(gemini_client, possible_fields, available_fields)
                )

                corrected_arguments = arguments.copy()

                argument_fields = arguments.get("fields")
                if isinstance(argument_fields, list):
                    corrected_field_names_map = loop.run_until_complete(
                        correct_typos_with_gemini(gemini_client, argument_fields, available_fields)
                    )
                    filtered_fields = [
                        corrected for original, corrected in corrected_field_names_map.items()
                        if corrected in available_fields.values()
                    ]
                    corrected_arguments["fields"] = filtered_fields

                if "sort_by" in arguments:
                    sort_by = arguments["sort_by"]
                    sort_by = next(
                        (f for f in available_fields.values() if f.lower() == sort_by.lower()),
                        sort_by
                    )
                    corrected_arguments["sort_by"] = sort_by

                if "sort_order" in arguments:
                    sort_order = arguments["sort_order"].lower()
                    if sort_order in ["asc", "desc"]:
                        corrected_arguments["sort_order"] = sort_order

                result = loop.run_until_complete(mcp_server.call_tool(tool_name, corrected_arguments))

                if isinstance(result, dict) and "error" in result:
                    api.abort(400, result["error"].get("message", "Unknown error"))

                content_text = result["content"][0]["text"]
                try:
                    parsed_json = json.loads(content_text)
                    return {"response": parsed_json}
                except json.JSONDecodeError:
                    return {"response": content_text}


            except Exception as e:
                logger.error(f"Error in chat endpoint: {e}")
                api.abort(500, "An error occurred while processing your request")
            finally:
                loop.close()

    return application


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)