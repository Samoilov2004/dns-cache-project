# pip install redis dnspython

import json
import sys
import time

import dns.resolver
import redis


def normalize_qname(name: str) -> str:
    name = name.strip().lower()
    if not name.endswith("."):
        name += "."
    return name


def main():
    if len(sys.argv) < 4:
        print("Usage: python scripts/fill_cache.py <qname> <qtype> <external_cache_ttl>")
        sys.exit(1)

    qname = normalize_qname(sys.argv[1])
    qtype = sys.argv[2].upper()
    external_cache_ttl = int(sys.argv[3])

    # запрос к вашему Unbound
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ["127.0.0.1"]
    resolver.port = 2053

    answer = resolver.resolve(qname, qtype)

    original_ttl = answer.rrset.ttl
    answers = []

    for item in answer:
        answers.append({
            "name": qname,
            "type": qtype,
            "ttl": original_ttl,
            "data": item.to_text()
        })

    now = int(time.time())

    payload = {
        "qname": qname,
        "qtype": qtype,
        "rcode": "NOERROR",
        "answers": answers,
        "original_ttl": original_ttl,
        "stored_at": now,
        "admin_expire_at": now + external_cache_ttl,
        "source": "fill_cache_script",
        "dnssec_status": "unchecked"
    }

    r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)
    key = f"dns:cache:{qname}:{qtype}"
    r.set(key, json.dumps(payload), ex=external_cache_ttl)

    print(f"Stored in Redis: {key}")
    print(f"Original TTL: {original_ttl}")
    print(f"External cache TTL: {external_cache_ttl}")


if __name__ == "__main__":
    main()
