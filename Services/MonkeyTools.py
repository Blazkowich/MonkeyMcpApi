import json
import logging

from Globals.Constants import valid_fields
from Services.MonkeyService import MonkeyService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonkeyTools:
    def __init__(self, monkey_service: MonkeyService):
        self._monkey_service = monkey_service

    async def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Execute a specific tool"""
        try:
            if tool_name == "get_monkeys":
                return await self._get_monkeys()
            elif tool_name == "get_monkeys_filtered":
                return await self._get_monkeys_filtered(arguments)
            elif tool_name == "get_monkey":
                return await self._get_monkey(arguments.get("name", ""))
            elif tool_name == "get_monkey_business":
                return await self._get_monkey_business()
            elif tool_name == "refresh_monkey_cache":
                return await self._refresh_monkey_cache()
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        except Exception as ex:
            logger.error(f"Failed to execute tool {tool_name}: {ex}")
            raise

    async def _get_monkeys(self) -> str:
        """Get all monkeys"""
        logger.info("Retrieving all monkeys")
        monkeys = await self._monkey_service.get_monkeys_async()
        result = json.dumps([monkey.to_dict() for monkey in monkeys], indent=2)
        logger.info(f"Successfully retrieved {len(monkeys)} monkeys")
        return result

    async def _get_monkeys_filtered(self, arguments: dict) -> str:
        """Get monkeys with filtering and sorting options"""
        logger.info("Retrieving filtered monkeys")
        monkeys = await self._monkey_service.get_monkeys_async()

        monkey_dicts = [monkey.to_dict() for monkey in monkeys]

        fields = arguments.get("fields", [])
        if fields:
            fields = [f for f in fields if f in valid_fields]
            if fields:
                monkey_dicts = [
                    {field: monkey.get(field) for field in fields}
                    for monkey in monkey_dicts
                ]

        sort_by = arguments.get("sort_by")
        sort_order = arguments.get("sort_order", "asc")

        if sort_by and sort_by in ["Name", "Location", "Details", "Image", "Population", "Latitude", "Longitude"]:
            reverse = sort_order.lower() == "desc"
            monkey_dicts.sort(key=lambda x: x.get(sort_by, 0), reverse=reverse)

        result = json.dumps(monkey_dicts, indent=2)
        logger.info(f"Successfully retrieved {len(monkey_dicts)} filtered monkeys")
        return result

    async def _get_monkey(self, name: str) -> str:
        """Get a specific monkey"""
        name = name.strip()
        if not name:
            raise ValueError("Monkey name cannot be null or empty")

        logger.info(f"Retrieving monkey: {name}")
        monkey = await self._monkey_service.get_monkey_async(name)
        result = json.dumps(monkey.to_dict(), indent=2)
        logger.info(f"Successfully retrieved monkey: {name}")
        return result

    @staticmethod
    async def _get_monkey_business() -> str:
        """Get monkey business emojis"""
        return "🐵🐵🐵"

    async def _refresh_monkey_cache(self) -> str:
        """Refresh monkey cache"""
        logger.info("Refreshing monkey cache")
        await self._monkey_service.refresh_cache_async()
        logger.info("Successfully refreshed monkey cache")
        return "Monkey cache refreshed successfully"
