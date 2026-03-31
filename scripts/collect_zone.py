#!/usr/bin/env python3
"""
collect_zone.py — 1.3.В: Сбор данных по зоне yandex.ru и генерация local-zones.conf

Скрипт:
  1. Запрашивает реальные DNS-записи yandex.ru через внешний резолвер (8.8.8.8).
  2. Показывает DNSSEC-информацию (RRSIG, DNSKEY) — доказательство, что зона подписана.
  3. Генерирует файл local-zones.conf с подставными IP (192.0.2.x, RFC 5737).

Использование:
  python3 scripts/collect_zone.py                  # вывод на экран
  python3 scripts/collect_zone.py --write          # перезаписать unbound/local-zones.conf
"""

import subprocess
import sys
import argparse
from pathlib import Path

ZONE = "yandex.ru"
RESOLVER = "8.8.8.8"        # публичный резолвер для сбора реальных данных
FAKE_IP_BASE = "192.0.2"    # RFC 5737 TEST-NET-1 — заведомо не принадлежит yandex.ru

RECORD_TYPES = ["A", "AAAA", "NS", "MX", "TXT"]
SUBDOMAINS = ["", "www", "mail", "maps"]

FAKE_IPS = {
    f"{ZONE}.":         f"{FAKE_IP_BASE}.1",
    f"www.{ZONE}.":     f"{FAKE_IP_BASE}.2",
    f"mail.{ZONE}.":    f"{FAKE_IP_BASE}.3",
    f"maps.{ZONE}.":    f"{FAKE_IP_BASE}.4",
}


def dig(name: str, rtype: str, dnssec: bool = False) -> str:
    cmd = ["dig", f"@{RESOLVER}", "+noall", "+answer", name, rtype]
    if dnssec:
        cmd.insert(2, "+dnssec")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
    return result.stdout.strip()


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def collect_and_print():
    section("1.3.А — DNSSEC-подписанность зоны .ru и yandex.ru")

    print(f"\n[DS-запись yandex.ru в зоне .ru — цепочка доверия]")
    out = dig(ZONE, "DS")
    print(out if out else "  (DS-запись отсутствует — DNSSEC на уровне домена не настроен)")

    print(f"\n[DNSKEY yandex.ru]")
    out = dig(ZONE, "DNSKEY")
    print(out if out else "  (DNSKEY отсутствует)")

    print(f"\n[RRSIG для A-записи yandex.ru — подтверждение подписи]")
    out = dig(ZONE, "A", dnssec=True)
    print(out if out else "  (RRSIG отсутствует)")

    print(f"\n[DS-запись .ru в корневой зоне — TLD подписан]")
    out = subprocess.run(
        ["dig", f"@{RESOLVER}", "+noall", "+answer", "ru.", "DS"],
        capture_output=True, text=True, timeout=10
    ).stdout.strip()
    print(out if out else "  (не получено)")

    section("1.3.В — Реальные записи зоны yandex.ru")

    real_records = {}
    for sub in SUBDOMAINS:
        fqdn = f"{sub}.{ZONE}." if sub else f"{ZONE}."
        for rtype in RECORD_TYPES:
            out = dig(fqdn.rstrip("."), rtype)
            if out:
                real_records.setdefault(fqdn, {})[rtype] = out
                print(f"\n[{fqdn} {rtype}]")
                print(out)

    section("1.3.В — Авторитетные серверы зоны (NS)")
    out = dig(ZONE, "NS")
    print(out if out else "  (нет данных)")

    return real_records


def generate_local_zones_conf() -> str:
    lines = [
        "# =============================================================================",
        f"# Автоматически сгенерировано скриптом collect_zone.py",
        f"# 1.3. Подмена зоны с DNSSEC — {ZONE}",
        "#",
        f"# {ZONE} находится под DNSSEC-подписанным TLD .ru.",
        "# Тип 'static': Unbound отвечает из local-data, не обращаясь",
        f"# к авторитетным серверам ns1.yandex.ru / ns2.yandex.ru.",
        "#",
        f"# Подставные IP из TEST-NET (RFC 5737, {FAKE_IP_BASE}.0/24).",
        f"# Реальные IP yandex.ru: 77.88.55.77, 77.88.55.88",
        "# =============================================================================",
        "",
        f'local-zone: "{ZONE}." static',
        "",
        "# A-записи с подставными адресами",
    ]

    for fqdn, fake_ip in FAKE_IPS.items():
        lines.append(f'local-data: "{fqdn} 300 IN A {fake_ip}"')

    lines += [
        "",
        "# NS-записи (реальные, подтверждают принадлежность зоны)",
        f'local-data: "{ZONE}. 300 IN NS ns1.yandex.ru."',
        f'local-data: "{ZONE}. 300 IN NS ns2.yandex.ru."',
        "",
        "# MX",
        f'local-data: "{ZONE}. 300 IN MX 10 mx.yandex.ru."',
        "",
        "# TXT SPF",
        f'local-data: "{ZONE}. 300 IN TXT \\"v=spf1 redirect=_spf.yandex.ru\\""',
        "",
    ]

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Сбор записей зоны и генерация local-zones.conf")
    parser.add_argument("--write", action="store_true",
                        help="Перезаписать unbound/local-zones.conf")
    args = parser.parse_args()

    collect_and_print()

    conf = generate_local_zones_conf()

    section("Сгенерированный local-zones.conf")
    print(conf)

    if args.write:
        out_path = Path(__file__).parent.parent / "unbound" / "local-zones.conf"
        out_path.write_text(conf)
        print(f"\n[OK] Записано в {out_path}")
        print("     Пересоберите контейнер: docker compose build unbound && docker compose up -d unbound")

    section("Команды для проверки (1.3.Г)")
    print(f"""
# 1. Запрос через наш резолвер — должен вернуть 192.0.2.1 (подставной IP):
dig @127.0.0.1 -p 2053 {ZONE} A +short

# 2. Запрос к реальному DNS — для сравнения (77.88.55.x):
dig @8.8.8.8 {ZONE} A +short

# 3. Убедиться, что resolver отвечает из локальной зоны (status: NOERROR, no AA flag):
dig @127.0.0.1 -p 2053 {ZONE} A

# 4. Несуществующий в local-data хост — должен вернуть NXDOMAIN:
dig @127.0.0.1 -p 2053 nonexistent.{ZONE} A

# 5. Трассировка через внешний резолвер — покажет реальные серверы зоны:
dig @8.8.8.8 {ZONE} A +trace +dnssec 2>&1 | head -40

# 6. Логи Unbound — убедиться, что local_zone_answer, а не upstream:
docker compose logs unbound | grep -E "yandex|local_zone"
""")


if __name__ == "__main__":
    main()
