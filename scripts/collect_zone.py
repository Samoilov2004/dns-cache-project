#!/usr/bin/env python3
"""
collect_zone.py — 1.3.В: Сбор данных по DNSSEC-подписанной зоне cloudflare.com
и генерация local-zones.conf для Unbound.

Скрипт:
  1. Проверяет, что cloudflare.com подписан DNSSEC:
     - DS
     - DNSKEY
     - RRSIG
  2. Собирает реальные DNS-записи по зоне через внешний резолвер.
  3. Генерирует local-zones.conf с локальной подменой IP-адресов
     на TEST-NET адреса 192.0.2.x (RFC 5737).

Использование:
  python3 scripts/collect_zone.py
  python3 scripts/collect_zone.py --write
"""

import argparse
import subprocess
from pathlib import Path

ZONE = "cloudflare.com"
RESOLVER = "8.8.8.8"
FAKE_IP_BASE = "192.0.2"

# Имена, которые будем собирать и локально описывать
NAMES = [
    f"{ZONE}.",
    f"www.{ZONE}.",
]

# Какие типы записей собирать для анализа
RECORD_TYPES = ["A", "AAAA", "NS", "MX", "TXT"]

FAKE_IPS = {
    f"{ZONE}.": f"{FAKE_IP_BASE}.1",
    f"www.{ZONE}.": f"{FAKE_IP_BASE}.2",
}


def run(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    return result.stdout.strip()


def dig(name: str, rtype: str, dnssec: bool = False) -> str:
    cmd = ["dig", f"@{RESOLVER}", "+noall", "+answer", name, rtype]
    if dnssec:
        cmd.insert(2, "+dnssec")
    return run(cmd)


def section(title: str):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def collect_dnssec_proof():
    section("1.3.А — Проверка, что cloudflare.com подписан DNSSEC")

    print("\n[DS-запись cloudflare.com в родительской зоне]")
    out = dig(ZONE, "DS", dnssec=True)
    print(out if out else "  (DS не получен)")

    print("\n[DNSKEY-записи cloudflare.com]")
    out = dig(ZONE, "DNSKEY", dnssec=True)
    print(out if out else "  (DNSKEY не получен)")

    print("\n[A +dnssec для cloudflare.com — наличие RRSIG]")
    out = dig(ZONE, "A", dnssec=True)
    print(out if out else "  (A/RRSIG не получены)")


def collect_real_records():
    section("1.3.В — Сбор реальных записей зоны")

    collected = {}

    for fqdn in NAMES:
        print(f"\n--- {fqdn} ---")
        collected[fqdn] = {}

        for rtype in RECORD_TYPES:
            out = dig(fqdn.rstrip("."), rtype)
            if out:
                collected[fqdn][rtype] = out
                print(f"\n[{rtype}]")
                print(out)

    return collected


def generate_local_zones_conf() -> str:
    lines = [
        "# =============================================================================",
        "# Автоматически сгенерировано collect_zone.py",
        f"# Локальная подмена DNSSEC-подписанной зоны {ZONE}",
        "#",
        "# ВАЖНО:",
        "# - зона выбрана как DNSSEC-подписанная;",
        "# - Unbound будет отвечать по ней локально;",
        "# - TEST-NET адреса (RFC 5737) используются специально,",
        "#   чтобы наглядно отличать локальный ответ от реального.",
        "# =============================================================================",
        "",
        "server:",
        f'    local-zone: "{ZONE}." static',
        f'    local-data: "{ZONE}. 300 IN A {FAKE_IPS[f"{ZONE}."]}"',
        f'    local-data: "www.{ZONE}. 300 IN A {FAKE_IPS[f"www.{ZONE}."]}"',
        "",
    ]
    return "\n".join(lines)


def print_check_commands():
    section("1.3.Г — Команды для проверки")

    print(f"""
# 1. Проверка DNSSEC у публичного DNS
dig @{RESOLVER} {ZONE} DS +dnssec
dig @{RESOLVER} {ZONE} DNSKEY +dnssec
dig @{RESOLVER} {ZONE} A +dnssec

# 2. Сравнение реального и локального ответа
dig @{RESOLVER} {ZONE} A +short
dig @127.0.0.1 -p 2053 {ZONE} A +short

# 3. Проверка локальной подмены для поддомена
dig @127.0.0.1 -p 2053 www.{ZONE} A +short

# 4. Проверка несуществующего имени внутри локальной зоны
dig @127.0.0.1 -p 2053 hack.{ZONE} A

# 5. Трассировка реального публичного разрешения
dig +trace {ZONE} A +dnssec | head -40

# 6. Проверка отсутствия внешнего разрешения через tcpdump
docker exec -it dns-unbound tcpdump -tttt -n -i any '(udp port 53 or tcp port 53)'

# 7. Логи Unbound
docker compose logs unbound | grep -i cloudflare
""")


def main():
    parser = argparse.ArgumentParser(
        description="Сбор данных по DNSSEC-подписанной зоне и генерация local-zones.conf"
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Записать результат в unbound/local-zones.conf"
    )
    args = parser.parse_args()

    collect_dnssec_proof()
    collect_real_records()

    conf = generate_local_zones_conf()

    section("Сгенерированный local-zones.conf")
    print(conf)

    if args.write:
        out_path = Path(__file__).parent.parent / "unbound" / "local-zones.conf"
        out_path.write_text(conf, encoding="utf-8")
        print(f"\n[OK] Записано в {out_path}")
        print("Пересоберите и перезапустите Unbound:")
        print("docker compose build unbound && docker compose up -d unbound")

    print_check_commands()


if __name__ == "__main__":
    main()
