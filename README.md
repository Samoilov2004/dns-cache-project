# dns-cache-project
<p>
  <a href="https://redis.io/">
    <img src="https://img.shields.io/badge/Redis-DD0031?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  </a>
  <a href="https://www.docker.com/">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  </a>
  <a href="https://nlnetlabs.nl/projects/unbound/about/">
    <img src="https://img.shields.io/badge/Unbound-0B0C2E?style=for-the-badge&logo=https%3A%2F%2Fraw.githubusercontent.com%2FSamoilov2004%2Fdns-cache-project%2Fmain%2Freport%2Fassets%2Funbound-icon.svg&logoColor=white" alt="Unbound">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=FFD43B" alt="Python">
  </a>
</p>

Проект посвящен размещению собственного DNS-резолвера, способного кэшировать DNS-ответы на отличное от TTL время. Также реализуем
при помощи собственного DNS-резолвера обход ограничений протокола DNSSEC.


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
