# -*- coding: utf-8 -*-
"""ANSI terminal renk kodları"""


class Colors:
    """Terminal renk kodları"""
    NAVY = "\033[38;2;0;0;128m"       # Lacivert - Başarısız denemeler
    RED = "\033[91m"                   # Kırmızı - Başarılı denemeler
    GREEN = "\033[92m"                 # Yeşil - Bilgi mesajları
    YELLOW = "\033[93m"               # Sarı - Uyarılar
    CYAN = "\033[96m"                 # Cyan - Başlıklar
    WHITE = "\033[97m"                # Beyaz - Genel metin
    BOLD = "\033[1m"                  # Kalın
    DIM = "\033[2m"                   # Soluk
    RESET = "\033[0m"                 # Sıfırla
    BG_RED = "\033[41m"               # Kırmızı arka plan
    BG_GREEN = "\033[42m"             # Yeşil arka plan
    BG_NAVY = "\033[48;2;0;0;128m"    # Lacivert arka plan
