from cache_core.service import DNSCacheService

def main():
    service = DNSCacheService()

    entry = service.get_response("yandex.ru", "A")
    if entry is None:
        print("CACHE MISS")
        return

    print("CACHE HIT")
    print(entry.to_dict())


if __name__ == "__main__":
    main()
