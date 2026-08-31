# -*- coding: utf-8 -*-
"""DVWA oturum yönetimi — giriş, CSRF token, güvenlik seviyesi"""

import re
import requests
import urllib3

from ..utils import Printer
from ..config import CSRF_TOKEN_PATTERN, PAGE_NAMES, DEFAULT_TIMEOUT

# SSL uyarılarını devre dışı bırak (yerel test ortamları için)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DVWASession:
    """DVWA oturum yönetimi sınıfı"""

    def __init__(self, base_url, username, password, security_level):
        # URL normalizasyonu: sondaki sayfa adlarını temizle
        base_url = base_url.rstrip("/")
        for page in PAGE_NAMES:
            if base_url.endswith("/" + page) or base_url.endswith(page):
                base_url = base_url[:base_url.rfind("/" + page)] if "/" + page in base_url else base_url.replace(page, "")
                break
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.security_level = security_level
        self.session = requests.Session()
        self.session.verify = False
        self.logged_in = False

    def get_csrf_token(self, url_or_text):
        """Sayfadan veya HTML metninden CSRF token'ı al"""
        try:
            # Eğer HTML metni verilmişse doğrudan kullan, değilse GET isteği yap
            if "<" in url_or_text and ">" in url_or_text:
                text = url_or_text
            else:
                response = self.session.get(url_or_text, timeout=DEFAULT_TIMEOUT)
                text = response.text
            match = re.search(CSRF_TOKEN_PATTERN, text)
            if match:
                return match.group(1)
        except Exception:
            pass
        return None

    def login(self):
        """DVWA'ya normal kimlik bilgileriyle giriş yap"""
        Printer.section("DVWA GİRİŞ")
        login_url = f"{self.base_url}/login.php"

        try:
            # Önce bağlantı testi yap
            Printer.info(f"Bağlantı test ediliyor: {self.base_url}")
            try:
                test_resp = self.session.get(self.base_url, timeout=DEFAULT_TIMEOUT, allow_redirects=True)
                Printer.info(f"Bağlantı başarılı (HTTP {test_resp.status_code})")
                # Eğer otomatik olarak login.php'ye yönlendirildiyse, URL'yi güncelle
                if "login.php" in test_resp.url:
                    login_url = test_resp.url
                    Printer.info(f"Login sayfasına yönlendirildi: {login_url}")
            except requests.ConnectionError:
                Printer.fail(f"Bağlantı kurulamadı: {self.base_url}")
                Printer.warning("DVWA'nın çalıştığından ve URL'in doğru olduğundan emin olun")
                return False

            # Login sayfasını al (CSRF token için)
            Printer.info(f"Login sayfası alınıyor: {login_url}")
            resp = self.session.get(login_url, timeout=DEFAULT_TIMEOUT)

            if resp.status_code != 200:
                Printer.fail(f"Login sayfasına erişilemedi (HTTP {resp.status_code})")
                return False

            # CSRF token'ı doğrudan response'dan çıkar (ek GET isteği yapmadan)
            token = self.get_csrf_token(resp.text)
            if not token:
                Printer.warning("CSRF token bulunamadı, tokensız deneniyor...")
            else:
                Printer.info(f"CSRF token alındı: {token[:16]}...")

            # Giriş yap
            login_data = {
                "username": self.username,
                "password": self.password,
                "Login": "Login",
            }
            if token:
                login_data["user_token"] = token

            Printer.info(f"Giriş yapılıyor: {self.username}:{self.password}")
            resp = self.session.post(login_url, data=login_data, timeout=DEFAULT_TIMEOUT,
                                    allow_redirects=True)

            Printer.info(f"Yanıt URL: {resp.url} (HTTP {resp.status_code})")

            # Giriş başarılı mı kontrol et - çoklu yöntem
            login_success = False

            # Yöntem 1: Login sayfasından uzaklaştık mı?
            if "login.php" not in resp.url:
                login_success = True
                Printer.info("Login sayfasından yönlendirildi")

            # Yöntem 2: Yanıtta "Login failed" yok ve "Welcome" veya menü var mı?
            if "Login failed" not in resp.text and "login_failed" not in resp.text:
                if any(kw in resp.text for kw in ["Welcome", "DVWA", "Logout", "logout",
                                                   "vulnerabilities", "security.php"]):
                    login_success = True

            # Yöntem 3: index.php'ye gidip kontrol et
            if not login_success:
                try:
                    check = self.session.get(f"{self.base_url}/index.php", timeout=DEFAULT_TIMEOUT)
                    if "login.php" not in check.url and any(
                        kw in check.text for kw in ["Welcome", "DVWA", "Logout", "vulnerabilities"]
                    ):
                        login_success = True
                except Exception:
                    pass

            if login_success:
                self.logged_in = True
                Printer.success("DVWA'ya başarıyla giriş yapıldı!")

                # Güvenlik seviyesini ayarla
                self._set_security_level(self.security_level)
                return True

            # Başarısız - debug bilgisi göster
            Printer.fail("Giriş başarısız oldu")
            if "Login failed" in resp.text:
                Printer.warning("Sunucu 'Login failed' yanıtı döndü - şifre/kullanıcı adı yanlış olabilir")
            if "login.php" in resp.url:
                Printer.warning("Login sayfasına geri yönlendirildi")
            return False

        except requests.ConnectionError:
            Printer.fail(f"Bağlantı kurulamadı: {self.base_url}")
            Printer.warning("DVWA'nın çalıştığından ve URL'in doğru olduğundan emin olun")
            return False
        except Exception as e:
            Printer.fail(f"Giriş hatası: {str(e)}")
            return False

    def _set_security_level(self, level="low"):
        """DVWA güvenlik seviyesini ayarla"""
        security_url = f"{self.base_url}/security.php"
        try:
            # CSRF token al
            token = self.get_csrf_token(security_url)
            data = {"security": level, "seclev_submit": "Submit"}
            if token:
                data["user_token"] = token

            self.session.post(security_url, data=data, timeout=DEFAULT_TIMEOUT)
            Printer.info(f"Güvenlik seviyesi '{level}' olarak ayarlandı")
        except Exception as e:
            Printer.warning(f"Güvenlik seviyesi ayarlanamadı: {str(e)}")
