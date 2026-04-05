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



## Документы

| | |
|---|---|
| [Презентация](report/main.pptx) | Итоговая презентация проекта |
| [Отчёт](report/main.docx) | Финальный отчёт |
| [Черновик](report/README.md) | Файл с поэтапным решением, но в черновом варианте|

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

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#0B1220",
    "primaryColor": "#111827",
    "primaryTextColor": "#E5E7EB",
    "primaryBorderColor": "#3B82F6",
    "lineColor": "#64748B",
    "fontFamily": "Inter, Arial, sans-serif",
    "fontSize": "16px"
  }
}}%%

flowchart TD

    %% CLIENT
    CLIENT["👤 Клиент"]

    %% ENTRY
    UNBOUND["🧠 Unbound<br/>Resolver"]

    %% MODULES
    PYMOD["🐍 PythonMod<br/>Redis логика"]
    VALIDATOR["🔐 DNSSEC валидатор"]
    ITERATOR["🌍 Рекурсивный резолвер"]

    %% DATA SOURCES
    LOCAL["📁 Local Zones"]
    REDIS["⚡ Redis Cache"]

    ROOT["🌐 Корневой DNS"]
    TLD["🌐 TLD - сервер"]
    AUTH["🌐 Авторитативный DNS"]

    %% FLOW

    CLIENT --> UNBOUND

    %% LOCAL ZONE CHECK
    UNBOUND -->|1. local-zone проверка| LOCAL
    LOCAL -->|hit| RESPONSE_LOCAL["📦 Ответ из локальной зоны"]

    %% PYTHONMOD
    UNBOUND -->|2. pythonmod hook| PYMOD
    PYMOD -->|redis hit| RESPONSE_REDIS["⚡ Ответ из Redis"]
    PYMOD -->|redis miss| ITERATOR

    %% RECURSION
    ITERATOR --> ROOT
    ROOT --> TLD
    TLD --> AUTH
    AUTH --> RESPONSE_AUTH["📡 DNS ответ"]

    %% DNSSEC
    RESPONSE_AUTH --> VALIDATOR
    VALIDATOR -->|validated| CACHE_STORE

    %% STORE
    CACHE_STORE["💾 Cache Pipeline"] --> REDIS
    CACHE_STORE --> UNBOUND_CACHE["🧩 Internal Cache"]

    %% RETURN
    RESPONSE_LOCAL --> CLIENT
    RESPONSE_REDIS --> CLIENT
    VALIDATOR --> CLIENT

    %% STYLES

    classDef client fill:#1E293B,stroke:#38BDF8,stroke-width:2px,color:#E0F2FE;
    classDef core fill:#111827,stroke:#3B82F6,stroke-width:2px,color:#E5E7EB;
    classDef module fill:#1F2937,stroke:#8B5CF6,stroke-width:2px,color:#DDD6FE;
    classDef data fill:#052E16,stroke:#10B981,stroke-width:2px,color:#D1FAE5;
    classDef ext fill:#3F1D2E,stroke:#F43F5E,stroke-width:2px,color:#FFE4E6;
    classDef result fill:#1E1B4B,stroke:#6366F1,stroke-width:2px,color:#E0E7FF;

    class CLIENT client;
    class UNBOUND core;

    class PYMOD,VALIDATOR,ITERATOR module;

    class LOCAL,REDIS,UNBOUND_CACHE data;

    class ROOT,TLD,AUTH ext;

    class RESPONSE_LOCAL,RESPONSE_REDIS,RESPONSE_AUTH result;
```
