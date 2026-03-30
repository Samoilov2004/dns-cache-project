## Запуск и проверка

```bash
docker compose up -d --build unbound
docker compose ps
```

Запуск логов, там не должно быть ничего критического
```bash
docker compose logs unbound
```

Проверка того, что все нормально работает и кешируется
```bash
dig @127.0.0.1 -p 2053 yandex.ru A
sleep 5
dig @127.0.0.1 -p 2053 yandex.ru A
```

Что делает модуль `redis_pythonmod`
- принимает запрос в Unbound
- если это A-запись
- строит ключ вида dns:cache:yandex.ru.:A
- смотрит Redis
- если есть запись:
  формирует DNS-ответ
  возвращает его клиенту
  пишет redis_hit в лог
- если записи нет:
  пишет redis_miss
  передает обработку дальше Unbound
