from cache_core.service import DNSCacheService

def main():
    service = DNSCacheService()

    key = service.save_response(
        qname="yandex.ru",
        qtype="A",
        rcode="NOERROR",
        answers=[
            {
                "name": "yandex.ru.",
                "type": "A",
                "ttl": 300,
                "data": "77.88.55.60"
            }
        ],
        original_ttl=300,
        source="manual",
        dnssec_status="unchecked",
        external_cache_ttl=3600,
        metadata={"note": "manual preload test"}
    )

    print(f"Saved test record under key: {key}")


if __name__ == "__main__":
    main()
