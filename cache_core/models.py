from dataclasses import dataclass, asdict, field
from typing import List, Dict, Any
import time


@dataclass
class DNSAnswerRecord:
    name: str
    type: str
    ttl: int
    data: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DNSCacheEntry:
    qname: str
    qtype: str
    rcode: str
    answers: List[DNSAnswerRecord]
    original_ttl: int
    stored_at: int
    admin_expire_at: int
    source: str
    dnssec_status: str = "unchecked"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "qname": self.qname,
            "qtype": self.qtype,
            "rcode": self.rcode,
            "answers": [a.to_dict() for a in self.answers],
            "original_ttl": self.original_ttl,
            "stored_at": self.stored_at,
            "admin_expire_at": self.admin_expire_at,
            "source": self.source,
            "dnssec_status": self.dnssec_status,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DNSCacheEntry":
        answers = [DNSAnswerRecord(**a) for a in data.get("answers", [])]
        return cls(
            qname=data["qname"],
            qtype=data["qtype"],
            rcode=data["rcode"],
            answers=answers,
            original_ttl=data["original_ttl"],
            stored_at=data["stored_at"],
            admin_expire_at=data["admin_expire_at"],
            source=data["source"],
            dnssec_status=data.get("dnssec_status", "unchecked"),
            metadata=data.get("metadata", {}),
        )

    def is_admin_expired(self) -> bool:
        return int(time.time()) >= self.admin_expire_at
