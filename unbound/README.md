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
