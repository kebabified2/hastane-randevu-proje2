# Hastane Randevu Sistemi

## Amaç
Basit bir masaüstü uygulamasıyla hastalar için doktor randevularını oluşturmak, görüntülemek ve iptal etmek.

## Dosya Yapısı

| Dosya | Rol |
|:---|:---|
| `hospital_system.py` | İş mantığı; `Patient`, `Doctor`, `Appointment`, `ReservationSystem` sınıfları. |
| `arayuz.py` | Tkinter arayüzü. Uygulamayı başlatır, örnek doktor ve saat verilerini sisteme ekler. |

## Gereksinimler

- Python 3.9+
- Tkinter (çoğu Python dağıtımında hazır gelir)

## Kurulum
```bash
1. Repoyu klonlayın
cd Desktop
git clone https://github.com/kebabified2/hastane-randevu-proje2

2. Çalıştır
python arac_kiralama_gui.py
```
## Uygulama
Sol üstte hasta bilgilerini, altta doktor seçimi ve müsait saat listesini göreceksiniz.
- Randevu Almak
   ``` Hasta adını ve 11 haneli TCʼsini girin. (Alan yalnızca rakam kabul eder.)
    Doktoru seçin. Liste kutusunda o doktora ait boş saatler görünür.
    İstediğiniz saati tıklayın (tarih alanı otomatik dolar) ve Randevu Al düğmesine basın.
   ```
- Randevu İptal Etmek
```
Aktif randevular listesinde bir satıra tıklayın ve Randevu İptal düğmesine basın.
```

# Hatırlatma

- TC: 11 haneli, sadece rakam.

- Çakışma kontrolü: Aynı hasta veya doktor için aynı tarihte ikinci randevu alınamaz.

- Doktor müsait değilse randevu oluşturulamaz.

# Sınırlamalar

- Çok kullanıcılı senaryo veya ağ erişimi yok.  

- Saat dilimi desteği yok; tarih‐saatler yerel sistem saatine göre alınır.

---
## Lisans
MIT
