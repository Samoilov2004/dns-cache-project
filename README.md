# DNS Cache Project

<p>
  <a href="https://redis.io/">
    <img src="https://img.shields.io/badge/Redis-DD0031?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  </a>
  <a href="https://www.docker.com/">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  </a>
  <a href="https://nlnetlabs.nl/projects/unbound/about/">
    <img src="https://img.shields.io/badge/Unbound-0B0C2E?style=for-the-badge&logoColor=white" alt="Unbound">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=FFD43B" alt="Python">
  </a>
</p>

Этот репозиторий содержит реализацию решения кейса "Кэширование DNS (Применение внешних баз данных для кэширования DNS записей на неограниченный срок)" в рамках направления «Системный анализ и суперкомпьютерное моделирование» конкурса «Твой проект» 2025/2026.

Проект демонстрирует возможности по:
- Продлению времени жизни (TTL) DNS-записей сверх установленного значения
- Использованию внешней базы данных (Redis) для кэширования DNS-ответов
- Обходу ограничений DNSSEC через локальную подмену DNS-зон


## Документы


| Материал    | Описание                                      | Файл                                                     |
| ----------- | --------------------------------------------- | -------------------------------------------------------- |
| Презентация | Итоговая презентация проекта                  | [PDF](report/main.pptx)<br>[PPTX](report/main.pdf) |
| Отчёт       | Финальный отчёт                               | [DOCX](report/main.docx)                                      |
| Черновик    | Файл с поэтапным решением в черновом варианте | [MD](report/README.md)                                     |

**Компоненты:**

| Компонент | Роль |
|---|---|
| **Unbound** | DNS-резолвер с поддержкой Python-модулей и локальных зон |
| **Redis** | Внешний кэш — хранит DNS-ответы дольше TTL |
| **Pythonmod** | Интеграция Unbound ↔ Redis, генерация зон |

## Структура репозитория

```
dns-cache-project/
├── unbound/
│   ├── unbound.conf          # основная конфигурация резолвера
│   ├── redis_pythonmod.py    # Python-модуль: интеграция с Redis
│   ├── local-zones.conf      # локальные зоны (переопределение DNSSEC)
│   ├── root.hints            # адреса корневых DNS-серверов
│   └── Dockerfile            # образ Unbound
├── redis/
│   └── redis.conf            # конфигурация Redis
├── scripts/
│   ├── fill_cache.py         # заполнение Redis DNS-записями
│   └── collect_zone.py       # сбор данных для локальных зон
├── report/
│   ├── README.md             # черновик отчёта
│   ├── main.docx             # финальный отчёт
│   ├── main.pptx             # презентация
│   └── assets/               # скриншоты и иллюстрации
└── docker-compose.yml        # инструкция запуска всего стека
```

## Схема рхитектуры DNS-резолвера с внешним кэшированием

![Scheme](report/assets/architecture_v2_dark_version.png)