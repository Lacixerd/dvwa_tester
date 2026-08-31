# 🛡️ DVWA Security Tester

**DVWA (Damn Vulnerable Web Application)** üzerinde otomatik güvenlik testleri gerçekleştiren modüler bir Python CLI aracı. XSS (Cross-Site Scripting), SQL Injection ve kimlik doğrulama bypass zafiyetlerini tespit eder.

> ⚠️ **Uyarı:** Bu araç yalnızca **eğitim ve yetkili güvenlik testleri** amacıyla geliştirilmiştir. İzinsiz sistemler üzerinde kullanılması yasalara aykırıdır.

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Proje Yapısı](#-proje-yapısı)
- [Gereksinimler](#-gereksinimler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Güvenlik Seviyeleri](#-güvenlik-seviyeleri)
- [Test Modülleri](#-test-modülleri)
- [Mimari](#-mimari)

---

## ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| **Reflected XSS** | 15 farklı payload ile reflected XSS zafiyet testi |
| **Stored XSS** | Guestbook üzerinden stored XSS testi |
| **SQL Injection** | Auth bypass, UNION, Boolean/Time-based Blind SQLi |
| **Login Bypass** | SQL Injection ile kimlik doğrulama atlatma denemeleri |
| **Canary Sistemi** | Her payload'a benzersiz ID atanarak doğru tespit sağlanır |
| **CSRF Token Yönetimi** | DVWA'nın CSRF korumalarını otomatik olarak handle eder |
| **Güvenlik Seviyesi Desteği** | `low`, `medium`, `high`, `impossible` seviyeleri |
| **Renkli Terminal Çıktısı** | ANSI renk kodları ile okunabilir sonuç raporlama |
| **Ayarlanabilir Zamanlama** | Payload'lar arası bekleme süresi yapılandırılabilir |

---

## 📁 Proje Yapısı

```
dvwa_tester/
├── __init__.py            # Paket tanımı
├── __main__.py            # python -m dvwa_tester desteği
├── main.py                # CLI giriş noktası (argparse)
├── config.py              # Yapılandırma sabitleri
│
├── core/                  # Çekirdek bileşenler
│   ├── __init__.py
│   ├── scanner.py         # Ana test orkestratörü
│   └── session.py         # DVWA oturum yönetimi (login, CSRF, güvenlik seviyesi)
│
├── modules/               # Test modülleri
│   ├── __init__.py
│   ├── base.py            # Tüm modüllerin temel sınıfı (BaseModule)
│   ├── login_bypass.py    # SQL Injection ile login bypass testleri
│   ├── sqli.py            # SQL Injection testleri
│   ├── xss_reflected.py   # Reflected XSS testleri
│   └── xss_stored.py      # Stored XSS testleri
│
├── payloads/              # Payload tanımları
│   ├── __init__.py
│   ├── login.py           # Login bypass payload'ları (6 adet)
│   ├── sqli.py            # SQL Injection payload'ları (16 adet)
│   └── xss.py             # XSS payload'ları (15 reflected + 3 stored)
│
└── utils/                 # Yardımcı araçlar
    ├── __init__.py
    ├── colors.py           # ANSI terminal renk kodları
    └── printer.py          # Renk kodlu çıktı fonksiyonları
```

---

## 🔧 Gereksinimler

- **Python** 3.7+
- **DVWA** çalışır durumda (lokal veya uzak sunucu)

### Python Bağımlılıkları

| Paket | Açıklama |
|---|---|
| `requests` | HTTP istekleri için |
| `urllib3` | SSL uyarı yönetimi |
| `re` (standart kütüphane) | Regex işlemleri |
| `argparse` (standart kütüphane) | CLI argüman ayrıştırma |

---

## 🚀 Kurulum

### 1. Projeyi klonlayın

```bash
git clone <repo-url>
cd dvwa_tester
```

### 2. Sanal ortam oluşturun (önerilir)

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
```

### 3. Bağımlılıkları yükleyin

```bash
pip install requests
```

### 4. DVWA'yı hazırlayın

DVWA'nın çalışır durumda olduğundan emin olun. Docker ile hızlıca başlatabilirsiniz:

```bash
docker run -d -p 80:80 vulnerables/web-dvwa
```

---

## 💻 Kullanım

> **Önemli:** Komutların tamamı projenin **kök dizininden** çalıştırılmalıdır (`inventiv - staj projesi/`). `dvwa_tester/` alt dizininin içinden çalıştırmayın.

```bash
# Doğru dizinde olduğunuzdan emin olun
cd "/Users/.../dvwa_tester"   # proje kök dizini

# Yanlış: dvwa_tester/ içinden çalıştırma → 'No module named dvwa_tester'
# Doğru: Kök dizinden çalıştırma ↓
```

### Temel Kullanım

```bash
python3 -m dvwa_tester --url http://localhost/dvwa
```

### Tüm Seçenekler

```bash
python3 -m dvwa_tester \
    --url http://localhost/dvwa \
    --username admin \
    --password password \
    --interval 3 \
    --security low
```

### CLI Argümanları

| Argüman | Kısaltma | Varsayılan | Açıklama |
|---|---|---|---|
| `--url` | `-u` | *(zorunlu)* | DVWA'nın base URL'i |
| `--username` | `-U` | `admin` | DVWA kullanıcı adı |
| `--password` | `-P` | `password` | DVWA şifresi |
| `--interval` | `-i` | `5` | Payload'lar arası bekleme süresi (saniye) |
| `--security` | `-s` | `low` | DVWA güvenlik seviyesi |

### Kullanım Örnekleri

```bash
# Varsayılan ayarlarla çalıştır
python3 -m dvwa_tester -u http://localhost/dvwa

# Özel kimlik bilgileri ile
python3 -m dvwa_tester -u http://localhost/dvwa -U admin -P password

# Hızlı tarama (2 saniye aralık)
python3 -m dvwa_tester -u http://localhost/dvwa -i 2

# Medium güvenlik seviyesinde test
python3 -m dvwa_tester -u http://localhost/dvwa -s medium

# Uzak sunucuda test
python3 -m dvwa_tester -u http://192.168.1.100/dvwa -i 3
```

---

## 🔒 Güvenlik Seviyeleri

DVWA'nın 4 güvenlik seviyesi desteklenir:

| Seviye | Koruma | Beklenen Sonuç |
|---|---|---|
| `low` | Filtre yok | Tüm saldırılar çalışır |
| `medium` | Basit filtreler | Bazı bypass'lar çalışır |
| `high` | `htmlspecialchars` / PDO | Çoğu saldırı engellenir |
| `impossible` | Tam koruma (referans) | Hiçbir saldırı çalışmaz |

---

## 🧪 Test Modülleri

### 1. Login Bypass (`LoginBypassModule`)

SQL Injection kullanarak DVWA login sayfasını bypass etmeyi dener.

- Her denemede **yeni HTTP session** açılır
- CSRF token otomatik olarak handle edilir
- **6 farklı** bypass payload'ı test edilir
- Başarılı bypass durumunda **KRİTİK SEVİYE** uyarısı verilir

**Örnek Payload'lar:**
```
admin' --
' OR '1'='1' --
' UNION SELECT 'admin','password' --
```

### 2. Reflected XSS (`XSSReflectedModule`)

GET parametresi üzerinden reflected XSS zafiyetlerini test eder.

- **Canary sistemi**: Her payload'a benzersiz rastgele ID eklenir
- HTML encoding kontrolü ile false-positive önlenir
- Tag filtreleme tespiti yapılır
- **15 farklı** payload (temel + filtre bypass)

**Örnek Payload'lar:**
```html
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
<ScRiPt>alert('XSS')</ScRiPt>        <!-- Büyük/küçük harf bypass -->
<scr<script>ipt>alert('XSS')</scr</script>ipt>  <!-- İç içe tag bypass -->
```

### 3. Stored XSS (`XSSStoredModule`)

DVWA Guestbook üzerinden stored XSS zafiyetlerini test eder.

- Hem **isim** hem **mesaj** alanlarında test yapılır
- Reflected XSS doğrulama motoru kullanılır
- **3 farklı** stored XSS payload'ı

### 4. SQL Injection (`SQLiModule`)

ID parametresi üzerinden SQL Injection zafiyetlerini test eder.

- **Auth Bypass**: `OR` tabanlı bypass denemeleri
- **Data Extraction**: `UNION SELECT` ile veri çıkarma
- **Boolean Blind**: `AND 1=1` / `AND 1=2` karşılaştırma
- **Time-based Blind**: `SLEEP()` ile zamanlama analizi
- Çıkarılan veriler tablo formatında gösterilir
- **16 farklı** SQL Injection payload'ı

**Örnek Payload'lar:**
```sql
' OR '1'='1
1' UNION SELECT user(),database() --
1' AND SLEEP(3) --
1' UNION SELECT user,password FROM users --
```

---

## 🏗️ Mimari

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   main.py   │────▶│ DVWAScanner  │────▶│   DVWASession   │
│  (CLI/Args) │     │ (Orkestratör)│     │ (Oturum Yönet.) │
└─────────────┘     └──────┬───────┘     └─────────────────┘
                           │
                    ┌──────┴──────┐
                    │  BaseModule │ (Soyut temel sınıf)
                    └──────┬──────┘
          ┌────────────────┼────────────────┐───────────────┐
          ▼                ▼                ▼               ▼
   ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌────────────┐
   │LoginByp. │    │XSS Reflect│    │XSS Stored│    │   SQLi     │
   │  Module  │    │  Module   │    │  Module  │    │  Module    │
   └──────────┘    └───────────┘    └──────────┘    └────────────┘
          │                │                │               │
          ▼                ▼                ▼               ▼
   ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌────────────┐
   │  login   │    │    xss    │    │   xss    │    │   sqli     │
   │ payloads │    │ payloads  │    │ payloads │    │  payloads  │
   └──────────┘    └───────────┘    └──────────┘    └────────────┘
```

### Temel Akış

1. **CLI** → `argparse` ile parametreler alınır
2. **DVWAScanner** → Oturum ve modülleri oluşturur
3. **DVWASession** → DVWA'ya giriş yapar, CSRF token ve güvenlik seviyesini yönetir
4. **Modüller** → Sırayla çalıştırılır, her biri kendi payload listesini test eder
5. **Sonuç Özeti** → Toplam test, başarılı/başarısız sayıları ve zafiyet raporu gösterilir

### Renk Kodlama Sistemi

| Renk | Anlam |
|---|---|
| 🔴 **Kırmızı** | Başarılı saldırı (zafiyet tespit edildi) |
| 🔵 **Lacivert** | Başarısız saldırı (güvenli) |
| 🟢 **Yeşil** | Bilgi mesajları |
| 🟡 **Sarı** | Uyarılar |
| 🔵 **Cyan** | Bölüm başlıkları |

---

## 📊 Örnek Çıktı

```
    ╔══════════════════════════════════════════════════════════════╗
    ║          ██████╗ ██╗   ██╗██╗    ██╗ █████╗                  ║
    ║          ██╔══██╗██║   ██║██║    ██║██╔══██╗                 ║
    ║          ██║  ██║██║   ██║██║ █╗ ██║███████║                 ║
    ║          ██║  ██║╚██╗ ██╔╝██║███╗██║██╔══██║                 ║
    ║          ██████╔╝ ╚████╔╝ ╚███╔███╔╝██║  ██║                ║
    ║          ╚═════╝   ╚═══╝   ╚══╝╚══╝ ╚═╝  ╚═╝               ║
    ║            ⚡ Güvenlik Test Aracı ⚡                         ║
    ╚══════════════════════════════════════════════════════════════╝

  ═════════════════════════════════════════════════════════════════
                      📊 TEST SONUÇ ÖZETİ
  ═════════════════════════════════════════════════════════════════

  Toplam Test         : 40
  Başarılı (Kırılgan) : 28
  Başarısız (Güvenli) : 12
  Başarı Oranı        : 70.0%

  XSS Başarılı        : 14
  SQLi Başarılı       : 12
  Auth Bypass         : 2

  ⚠  Toplam 28 zafiyet tespit edildi!
     Güvenlik seviyesini artırarak tekrar test edin.
```

---

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir. Yalnızca **yetkili test ortamlarında** kullanınız.
