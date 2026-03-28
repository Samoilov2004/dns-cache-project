# dns-cache-project
!!ТУТ НАДО ДОБАВИТЬ БЕЙДЖИ С ТЕХНОЛОГИЯМИ!!

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