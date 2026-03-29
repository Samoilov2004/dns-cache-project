# dns-cache-project
[![Redis](https://img.shields.io/badge/Redis-%23DD0031.svg?logo=redis&logoColor=white)](#)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](#)
[![Unbound](https://img.shields.io/badge/DNS-Unbound-blue?logo=https%3A%2F%2Fraw.githubusercontent.com%2FSamoilov2004%2Fdns-cache-project%2Fmain%2Freport%2Fassets%2Funbound.svg&logoColor=white)](#)


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


# Мысли про редис
В идеале хотелось бы вот такую формулировку - 
Для обеспечения сохранности внешнего кэша при перезапуске контейнеров и хоста Redis был настроен с персистентным Docker volume и журналированием AOF. Дополнительно использована политика автоматического перезапуска контейнера, что позволяет сохранять DNS-данные между перезапусками стенда.