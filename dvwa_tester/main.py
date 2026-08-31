#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI entry point"""

import argparse

from .core import DVWAScanner


def main():
    parser = argparse.ArgumentParser(
        description="DVWA Güvenlik Test Aracı - XSS & SQL Injection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python -m dvwa_tester --url http://localhost/dvwa
  python -m dvwa_tester --url http://localhost/dvwa --username admin --password password
  python -m dvwa_tester --url http://192.168.1.100/dvwa --interval 3
  python -m dvwa_tester --url http://localhost:8080 --security low

Güvenlik Seviyeleri:
  low        - Filtre yok (tüm saldırılar çalışır)
  medium     - Basit filtreler (bazı bypass'lar çalışır)
  high       - htmlspecialchars / PDO (güvenli)
  impossible - Tam koruma (referans implementasyon)
        """
    )

    parser.add_argument(
        "--url", "-u",
        required=True,
        help="DVWA'nın base URL'i (örn: http://localhost/dvwa)"
    )
    parser.add_argument(
        "--username", "-U",
        default="admin",
        help="DVWA kullanıcı adı (varsayılan: admin)"
    )
    parser.add_argument(
        "--password", "-P",
        default="password",
        help="DVWA şifresi (varsayılan: password)"
    )
    parser.add_argument(
        "--interval", "-i",
        type=int,
        default=5,
        help="Payload'lar arası bekleme süresi - saniye (varsayılan: 5)"
    )
    parser.add_argument(
        "--security", "-s",
        choices=["low", "medium", "high", "impossible"],
        default="low",
        help="DVWA güvenlik seviyesi (varsayılan: low)"
    )

    args = parser.parse_args()

    # Scanner oluştur ve çalıştır
    scanner = DVWAScanner(
        base_url=args.url,
        username=args.username,
        password=args.password,
        interval=args.interval,
        security=args.security,
    )
    scanner.run()


if __name__ == "__main__":
    main()
