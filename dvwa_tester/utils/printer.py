# -*- coding: utf-8 -*-
"""Renk kodlu terminal çıktı fonksiyonları"""

from datetime import datetime
from .colors import Colors


class Printer:
    """Renk kodlu terminal çıktıları için yardımcı sınıf"""

    @staticmethod
    def timestamp():
        """Zaman damgası döndür"""
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def success(msg):
        """Başarılı deneme mesajı (KIRMIZI)"""
        print(f"  {Colors.RED}{Colors.BOLD}[✓ BAŞARILI]{Colors.RESET} "
              f"{Colors.RED}{msg}{Colors.RESET} "
              f"{Colors.DIM}[{Printer.timestamp()}]{Colors.RESET}")

    @staticmethod
    def fail(msg):
        """Başarısız deneme mesajı (LACİVERT)"""
        print(f"  {Colors.NAVY}[✗ BAŞARISIZ]{Colors.RESET} "
              f"{Colors.NAVY}{msg}{Colors.RESET} "
              f"{Colors.DIM}[{Printer.timestamp()}]{Colors.RESET}")

    @staticmethod
    def info(msg):
        """Bilgi mesajı (YEŞİL)"""
        print(f"  {Colors.GREEN}[ℹ]{Colors.RESET} {Colors.WHITE}{msg}{Colors.RESET}")

    @staticmethod
    def warning(msg):
        """Uyarı mesajı (SARI)"""
        print(f"  {Colors.YELLOW}[⚠]{Colors.RESET} {Colors.YELLOW}{msg}{Colors.RESET}")

    @staticmethod
    def auth_bypass(msg):
        """Authentication bypass mesajı (KIRMIZI arka plan)"""
        print(f"\n  {Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}"
              f" 🔓 KİMLİK DOĞRULAMA AŞILDI! {Colors.RESET}")
        print(f"  {Colors.RED}{Colors.BOLD}{msg}{Colors.RESET}\n")

    @staticmethod
    def section(title):
        """Bölüm başlığı yazdır"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'━' * 65}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}  ▶ {title}{Colors.RESET}")
        print(f"{Colors.CYAN}{Colors.BOLD}{'━' * 65}{Colors.RESET}\n")
