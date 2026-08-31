# -*- coding: utf-8 -*-
"""Tüm test modüllerinin ortak arayüzü"""

import sys
import time

from ..utils import Colors


class BaseModule:
    """Tüm test modüllerinin temel sınıfı"""

    # Alt sınıflar tarafından tanımlanacak
    MODULE_NAME = "Base Module"

    def __init__(self, session, stats, interval):
        """
        Args:
            session: DVWASession instance
            stats: Paylaşılan istatistik sözlüğü
            interval: Payload'lar arası bekleme süresi (saniye)
        """
        self.session = session
        self.stats = stats
        self.interval = interval

    def run(self):
        """Test modülünü çalıştır — alt sınıflar implemente eder"""
        raise NotImplementedError("Alt sınıf run() metodunu implemente etmeli")

    def wait(self):
        """Belirlenen aralıkta bekle (geri sayım ile)"""
        for remaining in range(self.interval, 0, -1):
            sys.stdout.write(
                f"\r  {Colors.DIM}⏳ Sonraki payload için bekleniyor: "
                f"{remaining}s{Colors.RESET}  "
            )
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\r" + " " * 60 + "\r")
        sys.stdout.flush()
