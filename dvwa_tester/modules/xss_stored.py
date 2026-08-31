# -*- coding: utf-8 -*-
"""Stored XSS test modülü"""

import random

from .base import BaseModule
from .xss_reflected import XSSReflectedModule
from ..utils import Colors, Printer
from ..payloads import STORED_XSS_PAYLOADS


class XSSStoredModule(BaseModule):
    """Stored XSS testlerini çalıştıran modül"""

    MODULE_NAME = "STORED XSS TESTLERİ"

    def run(self):
        """Stored XSS testlerini çalıştır"""
        Printer.section(self.MODULE_NAME)

        if not self.session.logged_in:
            Printer.warning("DVWA'ya giriş yapılmamış, Stored XSS testleri atlanıyor")
            return

        xss_url = f"{self.session.base_url}/vulnerabilities/xss_s/"

        for i, xss in enumerate(STORED_XSS_PAYLOADS, 1):
            self.stats["total"] += 1

            # Benzersiz canary ile payload oluştur
            canary = f"sxss{random.randint(10000, 99999)}"
            test_name = xss["name"].replace("XSS", canary).replace("Stored XSS", canary)
            test_message = xss["message"].replace("XSS", canary).replace("Stored XSS", canary).replace("StoredXSS", canary)

            print(f"\n  {Colors.DIM}[{i}/{len(STORED_XSS_PAYLOADS)}] "
                  f"Stored XSS Denemesi{Colors.RESET}")
            print(f"  {Colors.DIM}İsim    : {xss['name'][:40]}{Colors.RESET}")
            print(f"  {Colors.DIM}Mesaj   : {xss['message'][:50]}{Colors.RESET}")
            print(f"  {Colors.DIM}Canary  : {canary}{Colors.RESET}")

            try:
                token = self.session.get_csrf_token(xss_url)
                data = {
                    "txtName": test_name,
                    "mtxMessage": test_message,
                    "btnSign": "Sign+Guestbook",
                }
                if token:
                    data["user_token"] = token

                resp = self.session.session.post(xss_url, data=data, timeout=10)

                # Canary'nin sayfada encode edilmeden var olup olmadığını kontrol et
                # Payload hangi alandaysa onu kontrol et
                check_payload = test_message if "<" in xss["message"] else test_name
                is_success, detail = XSSReflectedModule.check_xss_reflected(check_payload, resp.text)

                if is_success:
                    self.stats["success"] += 1
                    self.stats["xss_success"] += 1
                    Printer.success(f"{xss['description']} → {detail}")
                else:
                    self.stats["failed"] += 1
                    Printer.fail(f"{xss['description']} → {detail}")

            except Exception as e:
                self.stats["failed"] += 1
                Printer.fail(f"{xss['description']} → Hata: {str(e)}")

            if i < len(STORED_XSS_PAYLOADS):
                self.wait()
