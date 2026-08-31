# -*- coding: utf-8 -*-
"""Reflected XSS test modülü"""

import re
import random
import html as html_module

from .base import BaseModule
from ..utils import Colors, Printer
from ..payloads import XSS_PAYLOADS


class XSSReflectedModule(BaseModule):
    """Reflected XSS testlerini çalıştıran modül"""

    MODULE_NAME = "REFLECTED XSS TESTLERİ"

    @staticmethod
    def check_xss_reflected(payload, response_text):
        """XSS payload'ının encode edilmeden yansıyıp yansımadığını kontrol eder."""
        if payload in response_text:
            encoded = html_module.escape(payload)
            if encoded != payload:
                return True, "Payload encode edilmeden yansıtıldı!"
            else:
                return False, "Payload tehlikeli karakter içermiyor"
        
        encoded = html_module.escape(payload)
        if encoded in response_text:
            return False, "Payload HTML-encode edildi (XSS önlendi)"
        
        # Kısmi filtreleme kontrolü (tag kaldırılıp içerik bırakılmış olabilir)
        stripped = re.sub(r'<[^>]*>', '', payload)
        if stripped and stripped in response_text and stripped != payload:
            return False, "HTML tag'ları filtrelendi, içerik kaldı"
        
        return False, "Payload yansıtılmadı veya tamamen filtrelendi"

    def run(self):
        """Reflected XSS testlerini çalıştır"""
        Printer.section(self.MODULE_NAME)

        if not self.session.logged_in:
            Printer.warning("DVWA'ya giriş yapılmamış, XSS testleri atlanıyor")
            return

        xss_url = f"{self.session.base_url}/vulnerabilities/xss_r/"

        # Önce baseline al — temiz bir istek gönder, DVWA'nın normal sayfasını al
        Printer.info("Baseline alınıyor (normal sayfa içeriği)...")
        try:
            self.session.session.get(xss_url, params={"name": "baseline_test"}, timeout=10)
        except Exception:
            pass

        for i, xss in enumerate(XSS_PAYLOADS, 1):
            self.stats["total"] += 1
            payload = xss["payload"]
            desc = xss["description"]
            category = xss["category"]

            # Her payload'a benzersiz bir canary ekle (takip için)
            canary = f"c{random.randint(10000, 99999)}"
            test_payload = payload.replace("XSS", canary).replace("xss", canary)

            print(f"\n  {Colors.DIM}[{i}/{len(XSS_PAYLOADS)}] "
                  f"Kategori: {category}{Colors.RESET}")
            print(f"  {Colors.DIM}Payload : {payload[:60]}{'...' if len(payload) > 60 else ''}{Colors.RESET}")
            print(f"  {Colors.DIM}Canary  : {canary}{Colors.RESET}")

            try:
                # CSRF token al
                token = self.session.get_csrf_token(xss_url)
                params = {"name": test_payload}
                if token:
                    params["user_token"] = token

                resp = self.session.session.get(xss_url, params=params, timeout=10)

                # Canary tabanlı doğrulama
                is_success, detail = self.check_xss_reflected(test_payload, resp.text)

                if is_success:
                    self.stats["success"] += 1
                    self.stats["xss_success"] += 1
                    Printer.success(f"{desc} → {detail}")
                else:
                    self.stats["failed"] += 1
                    Printer.fail(f"{desc} → {detail}")

            except Exception as e:
                self.stats["failed"] += 1
                Printer.fail(f"{desc} → Hata: {str(e)}")

            # Belirlenen aralıkta bekle
            if i < len(XSS_PAYLOADS):
                self.wait()
