# NorthType

**NorthType**, Windows işletim sistemi için Python ve PySide6 kullanılarak geliştirilmiş, modern, hızlı ve güvenli bir akıllı metin kısayolu ve genişletme masaüstü uygulamasıdır. Yazım süreçlerinizi hızlandırmak, tekrarlayan metinleri otomatikleştirmek ve hassas verilerinizi güvenle saklamak için tasarlanmıştır.

---

## Özellikler

* **Arka Planda Kesintisiz Çalışma:** Global klavye dinleyicisi sayesinde belirlediğiniz tetikleyicileri anında algılar ve metne dönüştürür.
* **Hassas Veri Koruması (DPAPI):** Şifre veya özel notlar gibi hassas verilerinizi Windows DPAPI altyapısıyla güvenli bir şekilde şifreleyerek saklar.
* **Kategori Yönetimi:** Kısayollarınızı kategorilere ayırarak düzenleyin, arama ve filtreleme çubuğu ile dilediğinize saniyeler içinde ulaşın.
* **Çoklu Dil Desteği:** Türkçe ve İngilizce arayüz dil desteği (`i18n`).
* **Sistem Tepsisi (Tray) Entegrasyonu:** Görev çubuğunda arka planda çalışır, arayüze hızlı erişim sağlar ve Windows başlangıcında otomatik başlatılabilir.
* **İçe ve Dışa Aktarma:** Kısayollarınızı JSON formatında yedekleyin veya başka bir cihaza kolayca taşıyın.
* **Kullanım İstatistikleri:** Hangi kısayolu ne sıklıkla kullandığınızı ve ne kadar zaman kazandığınızı takip edin.

---

## Kullanılan Teknolojiler

* **Dil:** Python 3.13+
* **Arayüz Kütüphanesi:** PySide6 (Qt for Python)
* **Veritabanı:** SQLite
* **Sistem ve Donanım:** `keyboard`, `pyperclip`, Windows API (`ctypes`)

---

## Proje Yapısı

```text
NorthType/
│
├── data/
│   └── north_type.db          # Yerel SQLite veritabanı
├── ui/                        # Arayüz pencereleri ve modülleri
│   ├── category_dialog.py     # Kategori yönetim penceresi
│   ├── main_window.py         # Ana pencere ve arayüz mantığı
│   ├── settings_dialog.py     # Ayarlar ve yapılandırma
│   ├── shortcut_dialog.py     # Kısayol ekleme/düzenleme penceresi
│   ├── stats_dialog.py        # İstatistikler ekranı
│   ├── suggestion_popup.py    # Akıllı öneri açılır penceresi
│   └── tray.py                # Sistem tepsisi yöneticisi
├── database.py                # Veritabanı işlemleri ve JSON yönetimi
├── engine_interpreter.py      # Metin ve şablon yorumlayıcı
├── keyboard_engine.py         # Küresel klavye olay yöneticisi
├── i18n.py                    # Dil ve çeviri yönetimi
├── utils.py                   # Sistem araçları (Otomatik başlatma, ikon yönetimi)
├── utils_security.py          # Windows DPAPI şifreleme katmanı
├── main.py                    # Uygulama ana giriş noktası
└── requirements.txt           # Gerekli Python paketleri

```

---

## Kurulum ve Çalıştırma

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1. **Projeyi klonlayın veya indirin:**
```bash
git clone https://github.com/kullaniciadi/NorthType.git
cd NorthType

```


2. **Sanal ortam (venv) oluşturun ve aktifleştirin:**
```bash
python -m venv venv
# Windows için:
venv\Scripts\activate

```


3. **Gerekli bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt

```


4. **Uygulamayı başlatın:**
```bash
python main.py

```



---

## Kullanım

1. Uygulama açıldığında **"+ Kısayol Ekle"** butonuna tıklayın.
2. Tetikleyici kısayolu (Örn: `:mail`, `:merhaba`) ve bu kısayolun yerine yazılacak metni girin.
3. Eğer veri hassassa **"Hassas veri"** seçeneğini aktif ederek şifrelenmesini sağlayın.
4. Herhangi bir metin alanında (Not Defteri, Tarayıcı vb.) kısayolunuzu yazarak anında genişlemesini izleyin.

---

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Dilediğiniz gibi geliştirebilir ve kullanabilirsiniz.