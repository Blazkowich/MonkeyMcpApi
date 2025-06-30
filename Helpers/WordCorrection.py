import json
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def correct_typos_with_gemini(gemini_client, words, available_fields):
    prompt = (
        "You are a helpful assistant. The following is a list of possibly misspelled field names:\n"
        f"{words}\n"
        f"Here are the valid fields:\n{list(available_fields.values())}\n"
        "Correct each item (if needed) to the closest valid field name. "
        "Return a JSON object mapping original field names to corrected field names. "
        "If a field name cannot be corrected, omit it.\n\n"
        "Return only the JSON mapping."
    )

    response = await gemini_client.chat(prompt)

    try:
        json_match = re.search(r"```json\n(.*)\n```", response, re.DOTALL)
        if json_match:
            json_string = json_match.group(1)
        else:
            json_string = response

        return json.loads(json_string)
    except Exception as e:
        logger.error(f"Error correcting field names: {e}")
        return {}
