# dns-cache-project
[![Redis](https://img.shields.io/badge/Redis-DD0031?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Unbound](https://img.shields.io/badge/DNS-Unbound-1E90FF?style=for-the-badge&logo=https%3A%2F%2Fraw.githubusercontent.com%2FSamoilov2004%2Fdns-cache-project%2Fmain%2Freport%2Fassets%2Funbound.svg&logoColor=white)](https://nlnetlabs.nl/projects/unbound/about/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=FFD43B)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-in%20progress-yellow?style=for-the-badge)](#)


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
