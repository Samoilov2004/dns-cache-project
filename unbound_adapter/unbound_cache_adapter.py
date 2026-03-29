"""
Заготовка адаптера под Unbound pythonmod.

Идея:
- получить qname и qtype из запроса Unbound;
- спросить слой cache_core;
- если есть запись — вернуть ее в Unbound;
- если нет — передать управление стандартному резолвингу;
- после получения ответа сохранить его в Redis.

Конкретные callback-функции будут зависеть от pythonmod API Unbound
и будут добавлены после готовности конфигурации Unbound.
"""

from cache_core.service import DNSCacheService


class UnboundCacheAdapter:
    def __init__(self):
        self.cache = DNSCacheService()

    def lookup(self, qname: str, qtype: str):
        return self.cache.get_response(qname, qtype)

    def store(self, qname: str, qtype: str, rcode: str, answers, original_ttl: int):
        return self.cache.save_response(
            qname=qname,
            qtype=qtype,
            rcode=rcode,
            answers=answers,
            original_ttl=original_ttl,
            source="unbound",
        )
