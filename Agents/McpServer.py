from Services.MonkeyService import MonkeyService
from Services.MonkeyTools import MonkeyTools

class McpServer:
    def __init__(self, monkey_service: MonkeyService):
        self.monkey_service = monkey_service
        self.tools = MonkeyTools(monkey_service)

    async def call_tool(self, name: str, arguments: dict) -> dict:
        """Call a specific tool"""
        try:
            result = await self.tools.execute_tool(name, arguments)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ]
            }
        except Exception as ex:
            return {
                "error": {
                    "code": -1,
                    "message": str(ex)
                }
            }

