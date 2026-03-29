
## Назначение

Redis используется в проекте как внешнее хранилище DNS-ответов.

Основные функции Redis в рамках проекта:
- хранение DNS-ответов вне встроенного кэша резолвера;
- хранение записей на срок, определяемый администратором, а не только исходным DNS TTL;
- выдача ответов через промежуточный DNS proxy;
- сохранение кэша между перезапусками контейнеров и стенда.

## Формат ключей

Для хранения DNS-ответов используется пространство ключей следующего вида:

dns:cache:<fqdn>:<qtype>

Примеры:
- dns:cache:yandex.ru.:A
- dns:cache:cloudflare.com.:AAAA
- dns:cache:example.org.:TXT

Такой формат позволяет:
- явно отделить DNS-кэш от других служебных данных;
- удобно искать ключи;
- расширять структуру проекта без конфликтов имен.

---

## Формат значения

Значение хранится в виде JSON-объекта.

Рекомендуемые поля:
- qname — полное доменное имя;
- qtype — тип запроса;
- rcode — код ответа DNS;
- answers — список ресурсных записей;
- original_ttl — TTL, полученный от upstream;
- stored_at — время помещения записи в Redis;
- admin_expire_at — административный срок хранения;
- source — источник ответа;
- dnssec_status — состояние DNSSEC-проверки;
- metadata — дополнительные служебные поля при необходимости.

Пример логической структуры:

```json
{
  "qname": "yandex.ru.",
  "qtype": "A",
  "rcode": "NOERROR",
  "answers": [
    {
      "name": "yandex.ru.",
      "type": "A",
      "ttl": 300,
      "data": "77.88.55.60"
    }
  ],
  "original_ttl": 300,
  "stored_at": 1730000000,
  "admin_expire_at": 1730600000,
  "source": "upstream",
  "dnssec_status": "unchecked"
}
```

## Политика TTL

В проекте различаются два времени жизни:

1. DNS TTL — значение, полученное в DNS-ответе;
2. External cache TTL — административное время хранения во внешнем кэше Redis.

Redis хранит запись по административному TTL, который может быть больше исходного DNS TTL.

Пример:
- DNS TTL = 300 секунд;
- Redis TTL = 7 суток.

Это позволяет демонстрировать хранение DNS-ответов дольше стандартного TTL.

## Политика персистентности

Для обеспечения сохранности данных при перезапуске стенда Redis работает:
- с включенным AOF;
- с Docker named volume, подключенным к каталогу /data.

Это позволяет сохранять содержимое внешнего кэша при:
- перезапуске контейнера;
- остановке и повторном запуске docker compose;
- перезагрузке хоста (при сохранении Docker volume).

## `redis.conf`
Здесь напишу некие мысли по тому, зачем та или иная строчка
- `bind 0.0.0.0`
	Redis доступен внутри Docker-сети.
	Для локального проекта это нормально.

- `protected-mode yes`
	Дополнительная защита.
	Даже если порт случайно откроется не так, это полезная базовая мера.

- `dir /data`
	Все файлы persistence лежат в /data, куда мы подключили volume.

- `appendonly yes`
	Включает AOF, то есть запись операций в журнал.

- `appendfsync everysec`
	Хороший компромисс между надежностью и производительностью.

- `save ...`
	Это снапшоты RDB.

- `maxmemory 256mb`
	Для демоварианта проекта хватит.

- `maxmemory-policy noeviction`
	Redis не будет сам выкидывать записи.

## Что будет при перезагрузке?
- При docker compose restart redis
	данные останутся.

- При docker compose down и потом up
	данные останутся, если не делать down -v.

- При перезагрузке ноутбука
	данные останутся в Docker volume, но контейнер поднимется только если работает Docker.

## Как работать?
Чтобы поднять и проверить что поднялся
```bash
docker compose up -d redis
docker compose ps
```

Посмотреть логи
```bash
docker compose logs redis
```

Проверить `healthcheck/ping` - ожидается `PONG`
```bash
docker exec -it dns-redis redis-cli ping
```

Положить тестовый ключ и прочитать его 
```bash
docker exec -it dns-redis redis-cli SET dns:test "ok"
docker exec -it dns-redis redis-cli GET dns:test
```

Проверим возможности TTL-ключа - должно показать 120, а затем 150
```bash
docker exec -it dns-redis redis-cli SET dns:ttl:test "cached" EX 120
docker exec -it dns-redis redis-cli TTL dns:ttl:test
sleep 5
docker exec -it dns-redis redis-cli TTL dns:ttl:test
```

Проверка того, что json нормально хранится
```bash
docker exec -it dns-redis redis-cli SET dns:cache:yandex.ru.:A '{"qname":"yandex.ru.","qtype":"A","rcode":"NOERROR","answers":[{"name":"yandex.ru.","type":"A","ttl":300,"data":"77.88.55.60"}],"original_ttl":300,"stored_at":1730000000,"admin_expire_at":1730600000,"source":"manual","dnssec_status":"unchecked"}'
docker exec -it dns-redis redis-cli GET dns:cache:yandex.ru.:A
```

## Проверим отказоустойчивость
#### Данные переживают рестарт контейнера - после скрипта ключ должен остаться
```bash
docker exec -it dns-redis redis-cli SET dns:persist:test "survive"
docker exec -it dns-redis redis-cli GET dns:persist:test
docker compose restart redis
docker exec -it dns-redis redis-cli GET dns:persist:test
```

#### Данные переживают down/up
```bash
docker exec -it dns-redis redis-cli SET dns:compose:test "compose_persist"
docker compose down
docker compose up -d redis
docker exec -it dns-redis redis-cli GET dns:compose:test
```

Но не нужно делать 
```bash
docker compose down -v
```

иначе это удалит сам volume