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

> Кэширование DNS с помощью Redis — хранение записей дольше исходного TTL, локальное переопределение DNSSEC-зон.

## Архитектура

```mermaid
%%{init: {
  "theme": "base",
  "themeVariables": {
    "background": "#ffffff",
    "primaryColor": "#EAF2FF",
    "primaryTextColor": "#0F172A",
    "primaryBorderColor": "#2563EB",
    "lineColor": "#475569",
    "secondaryColor": "#FFF1F2",
    "tertiaryColor": "#F8FAFC",
    "fontFamily": "Inter, Arial, sans-serif",
    "fontSize": "16px"
  }
}}%%

flowchart LR
    client["Клиент"]

    subgraph unbound["DNS-резолвер Unbound"]
        direction TB
        u0["Ядро резолвера"]
        u1["Стандартный кэш"]
        u2["Python-модуль"]
        u3["Локальная зона"]
    end

    subgraph redis["Внешний кэш Redis"]
        direction TB
        r1[("Redis")]
        r2["Долговременное хранение"]
    end

    subgraph publicdns["Публичная DNS-инфраструктура"]
        direction TB
        p1["Корневые серверы"]
        p2["TLD-серверы"]
        p3["Авторитетные серверы"]
    end

    client -->|"DNS-запрос"| u0
    u0 --> u1
    u0 --> u2
    u0 --> u3
    u2 <-->|"кэш"| r1
    r1 --> r2
    u0 -->|"рекурсия"| p1
    p1 --> p2
    p2 --> p3
    p3 -->|"ответ"| u0
    u3 -->|"локальный ответ"| client
    u1 -->|"ответ из кэша"| client

    classDef clientStyle fill:#F8FAFC,stroke:#0F172A,stroke-width:2px,color:#0F172A;
    classDef unboundStyle fill:#EAF2FF,stroke:#2563EB,stroke-width:2px,color:#0F172A;
    classDef redisStyle fill:#FFF1F2,stroke:#DC2626,stroke-width:2px,color:#0F172A;
    classDef dnsStyle fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#0F172A;

    class client clientStyle;
    class u0,u1,u2,u3 unboundStyle;
    class r1,r2 redisStyle;
    class p1,p2,p3 dnsStyle;
```

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
└── docker-compose.yml        # запуск всего стека
```

## Документы

| | |
|---|---|
| [Презентация](report/main.pptx) | Слайды проекта |
| [Отчёт](report/main.docx) | Финальный отчёт |
| [Черновик](report/README.md) | Текстовый вариант |
