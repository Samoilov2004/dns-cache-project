import json
import logging
from typing import Optional

import redis

from .config import Settings
from .models import DNSCacheEntry


logger = logging.getLogger(__name__)


class RedisDNSStore:
    def __init__(self):
        self.client = redis.Redis(
            host=Settings.REDIS_HOST,
            port=Settings.REDIS_PORT,
            db=Settings.REDIS_DB,
            decode_responses=True,
        )

    def ping(self) -> bool:
        return self.client.ping()

    def get_raw(self, key: str) -> Optional[str]:
        return self.client.get(key)

    def get_ttl(self, key: str) -> int:
        return self.client.ttl(key)

    def set_entry(self, key: str, entry: DNSCacheEntry, ttl_seconds: int) -> None:
        value = json.dumps(entry.to_dict(), ensure_ascii=False)
        self.client.set(key, value, ex=ttl_seconds)
        logger.info("Saved cache entry: key=%s ttl=%s", key, ttl_seconds)

    def get_entry(self, key: str) -> Optional[DNSCacheEntry]:
        value = self.client.get(key)
        if value is None:
            return None

        data = json.loads(value)
        return DNSCacheEntry.from_dict(data)

    def delete(self, key: str) -> None:
        self.client.delete(key)

    def incr_stat(self, stat_name: str) -> None:
        self.client.incr(f"dns:stats:{stat_name}")
