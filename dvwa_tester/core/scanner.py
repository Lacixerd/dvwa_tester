# -*- coding: utf-8 -*-
"""Ana test orkestratörü — modülleri sırayla çalıştırır, istatistikleri toplar"""

from datetime import datetime

from .session import DVWASession
from ..utils import Colors, Printer
from ..modules import XSSReflectedModule, XSSStoredModule, SQLiModule, LoginBypassModule


class DVWAScanner:
    """DVWA güvenlik tarayıcısı — tüm modülleri yönetir"""

    def __init__(self, base_url, username="admin", password="password",
                 interval=5, security="low"):
        # Oturum yöneticisi oluştur
        self.dvwa_session = DVWASession(base_url, username, password, security)
        self.interval = interval

        # Paylaşılan istatistikler
        self.stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "xss_success": 0,
            "sqli_success": 0,
            "auth_bypass": 0,
        }

        # Test modüllerini oluştur
        self.modules = [
            LoginBypassModule(self.dvwa_session, self.stats, self.interval),
            XSSReflectedModule(self.dvwa_session, self.stats, self.interval),
            XSSStoredModule(self.dvwa_session, self.stats, self.interval),
            SQLiModule(self.dvwa_session, self.stats, self.interval),
        ]

    def _banner(self):
        """Başlangıç banner'ını yazdır"""
        session = self.dvwa_session
        banner = f"""
{Colors.RED}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║          ██████╗ ██╗   ██╗██╗    ██╗ █████╗                  ║
    ║          ██╔══██╗██║   ██║██║    ██║██╔══██╗                 ║
    ║          ██║  ██║██║   ██║██║ █╗ ██║███████║                 ║
    ║          ██║  ██║╚██╗ ██╔╝██║███╗██║██╔══██║                 ║
    ║          ██████╔╝ ╚████╔╝ ╚███╔███╔╝██║  ██║                ║
    ║          ╚═════╝   ╚═══╝   ╚══╝╚══╝ ╚═╝  ╚═╝               ║
    ║                                                              ║
    ║            ⚡ Güvenlik Test Aracı ⚡                         ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}
{Colors.DIM}  ─────────────────────────────────────────────────────────────────{Colors.RESET}
{Colors.CYAN}  Hedef URL  : {Colors.WHITE}{session.base_url}{Colors.RESET}
{Colors.CYAN}  Kullanıcı  : {Colors.WHITE}{session.username}{Colors.RESET}
{Colors.CYAN}  Aralık     : {Colors.WHITE}{self.interval} saniye{Colors.RESET}
{Colors.CYAN}  Güvenlik   : {Colors.WHITE}{session.security_level.upper()}{Colors.RESET}
{Colors.CYAN}  Tarih      : {Colors.WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}
{Colors.DIM}  ─────────────────────────────────────────────────────────────────{Colors.RESET}
"""
        print(banner)

    def print_summary(self):
        """Test sonuç özetini yazdır"""
        total = self.stats["total"]
        success = self.stats["success"]
        failed = self.stats["failed"]
        success_rate = (success / total * 100) if total > 0 else 0

        summary = f"""
{Colors.CYAN}{Colors.BOLD}{'═' * 65}{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}                    📊 TEST SONUÇ ÖZETİ{Colors.RESET}
{Colors.CYAN}{Colors.BOLD}{'═' * 65}{Colors.RESET}

  {Colors.WHITE}Toplam Test         : {Colors.BOLD}{total}{Colors.RESET}
  {Colors.RED}Başarılı (Kırılgan) : {Colors.BOLD}{success}{Colors.RESET}
  {Colors.NAVY}Başarısız (Güvenli) : {Colors.BOLD}{failed}{Colors.RESET}
  {Colors.YELLOW}Başarı Oranı        : {Colors.BOLD}{success_rate:.1f}%{Colors.RESET}

  {Colors.DIM}────────────────────────────────────────────{Colors.RESET}
  {Colors.RED}XSS Başarılı        : {Colors.BOLD}{self.stats['xss_success']}{Colors.RESET}
  {Colors.RED}SQLi Başarılı       : {Colors.BOLD}{self.stats['sqli_success']}{Colors.RESET}
  {Colors.RED}Auth Bypass         : {Colors.BOLD}{self.stats['auth_bypass']}{Colors.RESET}

{Colors.CYAN}{Colors.BOLD}{'═' * 65}{Colors.RESET}
"""
        print(summary)

        if self.stats["auth_bypass"] > 0:
            print(f"  {Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}"
                  f" ⚠  KİMLİK DOĞRULAMA AŞILDI - KRİTİK SEVİYE ZAFİYET! "
                  f"{Colors.RESET}\n")

        if success > 0:
            print(f"  {Colors.RED}⚠  Toplam {success} zafiyet tespit edildi!{Colors.RESET}")
            print(f"  {Colors.YELLOW}   Güvenlik seviyesini artırarak tekrar test edin.{Colors.RESET}\n")
        else:
            print(f"  {Colors.GREEN}✓  Hiçbir zafiyet tespit edilemedi.{Colors.RESET}")
            print(f"  {Colors.DIM}   (Güvenlik seviyesi yüksek olabilir){Colors.RESET}\n")

    def run(self):
        """Tüm testleri sırayla çalıştır"""
        self._banner()

        # DVWA'ya giriş yap
        if not self.dvwa_session.login():
            Printer.warning("Normal giriş başarısız - yalnızca login bypass testleri çalışacak")

        try:
            # Tüm modülleri sırayla çalıştır
            for module in self.modules:
                module.run()

        except KeyboardInterrupt:
            print(f"\n\n  {Colors.YELLOW}[!] Test kullanıcı tarafından durduruldu (Ctrl+C){Colors.RESET}")

        # Sonuç özeti
        self.print_summary()
