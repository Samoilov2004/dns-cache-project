import os

class Settings:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))

    # Административное время хранения по умолчанию (7 дней):
    EXTERNAL_CACHE_TTL = int(os.getenv("EXTERNAL_CACHE_TTL", "604800"))

    # Логический TTL, который можно потом возвращать клиенту
    RETURN_TTL = int(os.getenv("RETURN_TTL", "60"))
