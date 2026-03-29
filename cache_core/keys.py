def normalize_qname(qname: str) -> str:
    qname = qname.strip().lower()
    if not qname.endswith("."):
        qname += "."
    return qname


def normalize_qtype(qtype: str) -> str:
    return qtype.strip().upper()


def build_cache_key(qname: str, qtype: str) -> str:
    qname = normalize_qname(qname)
    qtype = normalize_qtype(qtype)
    return f"dns:cache:{qname}:{qtype}"
