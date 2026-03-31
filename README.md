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

Проект посвящён исследованию DNS-кэширования и разработке собственного DNS-стенда на базе **Unbound**, **Redis** и **Docker**.

В рамках работы реализуется:
- проверка стандартного кэширования DNS-ответов;
- подключение внешнего кэша для хранения записей дольше исходного TTL;
- ответы резолвера из внешней базы данных;
- локальное переопределение DNSSEC-подписанной зоны на уровне собственного резолвера.

---

## О проекте

Этот репозиторий создан в рамках проектного кейса по теме:

**«Кэширование DNS (Применение внешних баз данных для кэширования DNS записей на неограниченный срок)»**

Цель проекта — показать, как собственный DNS-резолвер может:
- кэшировать DNS-ответы стандартными средствами;
- использовать внешний кэш Redis;
- хранить записи дольше исходного DNS TTL;
- отвечать из своей локальной базы данных;
- локально переопределять DNSSEC-подписанную зону.

---

## Для кого этот репозиторий

Репозиторий предназначен для:
- жюри и экспертов, проверяющих проект;
- участников команды;
- тех, кто хочет воспроизвести проект локально;
- всех, кто интересуется практикой DNS, Unbound и внешним кэшированием.

---

## Что находится в репозитории

Основные материалы проекта:

- **конфигурация Unbound**;
- **конфигурация Redis**;
- **Python-скрипты для генерации и подготовки данных**;
- **локальные зоны для подмены ответов**;
- **отчёт, скриншоты и демонстрационные материалы**.

---

## Где находится отчёт

Основной отчёт и сопутствующие материалы расположены в папке:

```text
report/
```

Там расположен черновик отчета - `README.md` и финальные версии оформленной работы и презентации - файлы `main`

## Архитектура
Проект построен вокруг трёх основных компонентов:

- **Unbound** — DNS-резолвер;
- **Redis** — внешний кэш DNS-ответов;
- **Pythonmod** — вспомогательная логика для интеграции, подготовки данных и генерации локальных зон.

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
    client["Клиент / пользовательское приложение"]

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
        r2["Долговременное хранение DNS-ответов"]
    end

    subgraph publicdns["Публичная DNS-инфраструктура"]
        direction TB
        p1["Корневые DNS-серверы"]
        p2["TLD-серверы"]
        p3["Авторитетные DNS-серверы"]
    end

    note1["Хранение записей дольше исходного TTL"]
    note2["Локальное переопределение DNSSEC-подписанной зоны"]

    client -->|"DNS-запрос"| u0

    u0 --> u1
    u0 --> u2
    u0 --> u3

    u2 <-->|"поиск в кэше / выдача ответа"| r1
    r1 --> r2

    u0 -->|"рекурсивное разрешение"| p1
    p1 --> p2
    p2 --> p3
    p3 -->|"DNS-ответ"| u0

    u3 -->|"локальный ответ"| client
    u1 -->|"ответ из кэша"| client

    r2 -.-> note1
    u3 -.-> note2

    classDef clientStyle fill:#F8FAFC,stroke:#0F172A,stroke-width:2px,color:#0F172A;
    classDef unboundStyle fill:#EAF2FF,stroke:#2563EB,stroke-width:2px,color:#0F172A;
    classDef redisStyle fill:#FFF1F2,stroke:#DC2626,stroke-width:2px,color:#0F172A;
    classDef dnsStyle fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#0F172A;
    classDef noteStyle fill:#FFFBEB,stroke:#D97706,stroke-width:1.5px,color:#78350F,stroke-dasharray: 4 4;

    class client clientStyle;
    class u0,u1,u2,u3 unboundStyle;
    class r1,r2 redisStyle;
    class p1,p2,p3 dnsStyle;
    class note1,note2 noteStyle;
```
