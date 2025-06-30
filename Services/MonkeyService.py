from datetime import datetime
from threading import Lock
from typing import Optional, List
from Models.Monkey import Monkey
from Services.MonkeyNotFoundException import MonkeyNotFoundException
from Services.MonkeyServiceOptions import MonkeyServiceOptions
import logging, requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonkeyService:
    def __init__(self, options: MonkeyServiceOptions):
        self._options = options
        self._cached_monkeys: Optional[List[Monkey]] = None
        self._last_cache_update = datetime.min
        self._cache_lock = Lock()

    async def get_monkeys_async(self) -> List[Monkey]:
        """Get all monkeys, refreshing cache if needed"""
        await self._ensure_cache_is_current()
        return self._cached_monkeys if self._cached_monkeys else []

    async def get_monkey_async(self, name: str) -> Monkey:
        """Get a specific monkey by name"""
        if not name or not name.strip():
            raise ValueError("Monkey name cannot be null or empty")

        monkeys = await self.get_monkeys_async()
        monkey = next((m for m in monkeys if m.Name.lower() == name.lower()), None)

        if not monkey:
            raise MonkeyNotFoundException(name)

        return monkey

    async def refresh_cache_async(self):
        """Force refresh the monkey cache"""
        with self._cache_lock:
            await self._load_monkeys_from_api()

    async def _ensure_cache_is_current(self):
        """Ensure cache is current, refresh if expired"""
        if self._is_cache_expired():
            await self.refresh_cache_async()

    def _is_cache_expired(self) -> bool:
        """Check if the cache has expired"""
        return (self._cached_monkeys is None or
                datetime.now() - self._last_cache_update > self._options.cache_expiration)

    async def _load_monkeys_from_api(self):
        """Load monkeys from the API"""
        try:
            logger.info(f"Loading monkeys from API: {self._options.api_url}")

            if not self._options.api_url:
                raise ValueError("ApiUrl must be configured in MonkeyServiceOptions")

            response = requests.get(self._options.api_url)
            response.raise_for_status()

            monkey_data = response.json()
            self._cached_monkeys = [Monkey.from_dict(data) for data in monkey_data]
            self._last_cache_update = datetime.now()

            logger.info(f"Successfully loaded {len(self._cached_monkeys)} monkeys")

        except Exception as ex:
            logger.error(f"Failed to load monkeys from API: {ex}")
            self._cached_monkeys = self._cached_monkeys or []