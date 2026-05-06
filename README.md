# 🤖 Telegram PDF Özetleyici Bot (Docker + Huginn + Ollama)

Bu proje, kullanıcının Telegram üzerinden gönderdiği PDF dosyalarını otomatik olarak yakalayan, yerel bir yapay zeka (LLM) modeli kullanarak içeriği analiz eden ve kullanıcıya Türkçe özetini geri gönderen uçtan uca bir otomasyon hattıdır (pipeline).

## 🚀 Proje Amacı
Bu çalışmanın temel amacı; **Docker** konteyner mimarisi, **Huginn** otomasyon ajanları ve yerel çalışan bir **LLM (Ollama)** modelini birbirine entegre ederek, bulut servislerine ihtiyaç duymadan (privacy-first) çalışan bir yapay zeka asistanı oluşturmaktır.

## 🛠️ Kullanılan Teknolojiler ve Mimari
Sistem 4 ana bileşenden oluşmaktadır:
1.  **Telegram Bot API:** Kullanıcı ile arayüz etkileşimini sağlar.
2.  **Huginn (Workflow Automation):** Boru hattının (pipeline) yönetimini yapar. Veriyi Telegram'dan çeker, işlenmesi için Python servisine gönderir ve sonucu tekrar iletir.
3.  **Python (Flask Processor):** Arka planda PDF dosyalarını indirir, metinleri ayıklar (PyPDF2) ve yapay zeka modeline uygun prompt hazırlar.
4.  **Ollama (Local AI):** `qwen2:0.5b` modelini kullanarak internete ihtiyaç duymadan metin özetleme işlemini gerçekleştirir.



## 📋 Sistem Nasıl Çalışır? (Akış Şeması)
1.  **Giriş:** Kullanıcı bota bir PDF dosyası gönderir.
2.  **Yakalama:** Huginn `Website Agent`, Telegram API üzerinden yeni dökümanları tespit eder.
3.  **İşleme:** Veriler Docker ağındaki `pdf-processor` (Python) servisine iletilir.
4.  **Analiz:** Python servisi PDF'i okur ve metni Docker üzerinden `Ollama` servisine gönderir.
5.  **Özet:** Ollama, PDF içeriğini analiz edip Türkçe bir özet üretir.
6.  **Çıkış:** Özet metni Huginn üzerinden tekrar biçimlendirilerek (`EventFormattingAgent`) kullanıcıya Telegram mesajı olarak gönderilir.

## ⚙️ Kurulum ve Çalıştırma

### 1. Docker ile Sistemi Ayağa Kaldırma
Proje klasöründe terminali açarak aşağıdaki komutu çalıştırmanız yeterlidir:
```bash
docker-compose up -d
```
Bu komut Huginn, Ollama ve Python Processor servislerini ayağa kaldıracaktır.

### 2. Huginn Senaryosunu İçe Aktarma
* `localhost:3000` adresinden Huginn paneline girin.
* `Scenarios` sekmesinden `Import` seçeneğine tıklayın.
* Klasördeki `huginn_senaryo.json` dosyasını seçip içeri aktarın.

### 3. Yapılandırma
* İçe aktarılan senaryo içindeki `2- PDF Dinleyici` ve `5- Telegrama Ilet` ajanlarındaki `auth_token` kısımlarına kendi Telegram Bot Token'ınızı yazın.

## 📄 Proje Dosyaları
* `docker-compose.yml`: Servislerin orkestrasyonu.
* `/processor`: PDF işleme ve AI iletişim kodları (Python/Flask).
* `huginn_senaryo.json`: Otomasyon ajanlarının konfigürasyon yedeği.
