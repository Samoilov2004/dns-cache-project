# dns-cache-project
<p align="left">
  <a href="https://redis.io/">
    <img src="https://cdn.simpleicons.org/redis/DD0031" alt="Redis" height="40">
  </a>
  &nbsp;&nbsp;
  <a href="https://www.docker.com/">
    <img src="https://cdn.simpleicons.org/docker/2496ED" alt="Docker" height="40">
  </a>
  &nbsp;&nbsp;
  <a href="https://nlnetlabs.nl/projects/unbound/about/">
    <img src="./report/assets/unbound.svg" alt="Unbound" height="40">
  </a>
  &nbsp;&nbsp;
  <a href="https://www.python.org/">
    <img src="https://cdn.simpleicons.org/python/3776AB" alt="Python" height="40">
  </a>
</p>



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
