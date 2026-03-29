from cache_core.service import DNSCacheService


def main():
    service = DNSCacheService()
    ttl = service.get_cache_ttl("yandex.ru", "A")
    print(f"Redis TTL for yandex.ru A: {ttl}")


if __name__ == "__main__":
    main()
