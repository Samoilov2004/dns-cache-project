# dns-cache-project
проект по днс

Думаю что структура будет +- такая

dns-cache-project/
│
├─ README.md
├─ docker-compose.yml
├─ report/
│  ├─ report.pdf
│  ├─ screenshots/
│  └─ experiments.md
│
├─ unbound/
│  └─ unbound.conf
│
├─ redis/
│  └─ redis.conf
│
├─ proxy/
│  ├─ app.py
│  ├─ requirements.txt
│  └─ cache_logic.py
│
├─ scripts/
│  ├─ test_yandex.sh
│  ├─ fill_cache.py
│  └─ tcpdump_demo.sh
│
└─ zones/
   └─ local_override.zone