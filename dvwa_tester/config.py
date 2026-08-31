# -*- coding: utf-8 -*-
"""Yapılandırma sabitleri"""

# Varsayılan ayarlar
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "password"
DEFAULT_INTERVAL = 5
DEFAULT_SECURITY = "low"
DEFAULT_TIMEOUT = 10

# URL normalizasyonunda temizlenecek sayfa adları
PAGE_NAMES = ["login.php", "index.php", "setup.php", "security.php"]

# CSRF token regex deseni
CSRF_TOKEN_PATTERN = r"user_token.*?value=['\"]([a-f0-9]+)['\"]"

# SQL hata desenleri (SQLi tespiti için)
SQL_ERROR_PATTERNS = [
    "mysql_", "mysqli_", "sql syntax", "warning:",
    "error in your sql", "unclosed quotation",
    "mysql_fetch", "num_rows", "mysql_num_rows"
]
