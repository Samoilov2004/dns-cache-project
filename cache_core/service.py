import logging
import time
from typing import List, Optional, Dict, Any

from .config import Settings
from .keys import build_cache_key, normalize_qname, normalize_qtype
from .models import DNSAnswerRecord, DNSCacheEntry
from .redis_store import RedisDNSStore


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

logger = logging.getLogger(__name__)


class DNSCacheService:
    def __init__(self, store: Optional[RedisDNSStore] = None):
        self.store = store or RedisDNSStore()

    def save_response(
        self,
        qname: str,
        qtype: str,
        rcode: str,
        answers: List[Dict[str, Any]],
        original_ttl: int,
        source: str = "upstream",
        dnssec_status: str = "unchecked",
        external_cache_ttl: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        qname = normalize_qname(qname)
        qtype = normalize_qtype(qtype)
        key = build_cache_key(qname, qtype)

        now = int(time.time())
        ttl_seconds = external_cache_ttl or Settings.EXTERNAL_CACHE_TTL

        answer_models = [
            DNSAnswerRecord(
                name=a["name"],
                type=a["type"],
                ttl=int(a["ttl"]),
                data=a["data"],
            )
            for a in answers
        ]

        entry = DNSCacheEntry(
            qname=qname,
            qtype=qtype,
            rcode=rcode,
            answers=answer_models,
            original_ttl=int(original_ttl),
            stored_at=now,
            admin_expire_at=now + ttl_seconds,
            source=source,
            dnssec_status=dnssec_status,
            metadata=metadata or {},
        )

        self.store.set_entry(key, entry, ttl_seconds=ttl_seconds)
        self.store.incr_stat("cache_store")

        logger.info(
            "cache_store key=%s qname=%s qtype=%s rcode=%s",
            key, qname, qtype, rcode
        )
        return key

    def get_response(self, qname: str, qtype: str) -> Optional[DNSCacheEntry]:
        qname = normalize_qname(qname)
        qtype = normalize_qtype(qtype)
        key = build_cache_key(qname, qtype)

        entry = self.store.get_entry(key)
        if entry is None:
            self.store.incr_stat("cache_miss")
            logger.info("cache_miss key=%s", key)
            return None

        if entry.is_admin_expired():
            self.store.incr_stat("cache_stale")
            logger.info("cache_stale key=%s", key)
            return None

        self.store.incr_stat("cache_hit")
        logger.info("cache_hit key=%s", key)
        return entry

    def get_cache_ttl(self, qname: str, qtype: str) -> int:
        key = build_cache_key(qname, qtype)
        return self.store.get_ttl(key)

    def delete_response(self, qname: str, qtype: str) -> None:
        key = build_cache_key(qname, qtype)
        self.store.delete(key)
        logger.info("cache_delete key=%s", key)
