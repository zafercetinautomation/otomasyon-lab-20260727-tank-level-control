# TwinCAT Tank Seviye Kontrolü

Beckhoff TwinCAT 3 üzerinde iki seviye sensörüyle otomatik tank dolumu,
histerezis, vana kontrolü ve sensör tutarsızlığı alarmını öğreten Türkçe eğitim
projesi. Aynı kontrol mantığı Python simülasyonuyla PLC donanımı olmadan
denenebilir.

> Bu proje eğitim ve simülasyon amaçlıdır.

## Neler öğreneceksiniz?

- Alt ve üst seviye sensörleriyle dolum sırası kurma
- Histerezis kullanarak vananın sık açılıp kapanmasını önleme
- `R_TRIG` ile başlatma ve alarm sıfırlama darbelerini yakalama
- Üst sensör aktifken alt sensör pasifse sensör hatası üretme
- PLC kontrol mantığını Python birim testleriyle doğrulama

## Kontrol senaryosu

1. Otomatik mod açıkken `bStart` darbesi çevrimi etkinleştirir.
2. Tank üst seviyeye ulaşmadıysa dolum vanası açılır.
3. Üst seviye sensörü aktif olduğunda vana kapanır ve tank dolu bilgisi oluşur.
4. Seviye yalnızca üst sensörün altına düştüğünde vana hemen açılmaz.
5. Seviye alt sensörün de altına düştüğünde yeni dolum otomatik başlar.
6. Üst sensör aktifken alt sensör pasifse tutarsızlık alarmı kilitlenir.
7. Alarm, sensörler tutarlı ve çevrim duruyken sıfırlanabilir.

## Hızlı başlangıç

Python 3.11 veya daha yeni bir sürümle:

```bash
python3 src/main.py
python3 -m unittest discover -s tests -v
```

Örnek çıktı:

```text
Başlatıldı | vana=AÇIK | alt=0 | üst=0 | dolu=0 | hata=0
Alt seviyeye ulaştı | vana=AÇIK | alt=1 | üst=0 | dolu=0 | hata=0
Tank doldu | vana=KAPALI | alt=1 | üst=1 | dolu=1 | hata=0
Histerezis bölgesi | vana=KAPALI | alt=1 | üst=0 | dolu=0 | hata=0
Yeni dolum | vana=AÇIK | alt=0 | üst=0 | dolu=0 | hata=0
```

## TwinCAT 3'e aktarma

1. TwinCAT XAE içinde **TwinCAT Project → Add New Item → Standard PLC Project**
   ile bir PLC projesi oluşturun.
2. `PLC` altındaki `MAIN` programını açın.
3. [`plc/MAIN.st`](plc/MAIN.st) içeriğini `MAIN` programına aktarın.
4. Projeyi derleyin ve simülasyon hedefinde oturum açın.
5. Watch penceresinden girişleri değiştirerek kontrol senaryosunu izleyin.

Beckhoff'un resmî başlangıç kaynağı:
[TwinCAT 3 PLC tanıtımı](https://infosys.beckhoff.com/content/1033/tc3_system/2525041803.html)

## Değişkenler

| Değişken | Tür | Yön | Açıklama |
|---|---|---|---|
| `bAutoMode` | `BOOL` | Giriş | Otomatik kontrolü etkinleştirir |
| `bStart` | `BOOL` | Giriş | Dolum çevrimini başlatır |
| `bStop` | `BOOL` | Giriş | Çevrimi öncelikli olarak durdurur |
| `bLowLevelSensor` | `BOOL` | Giriş | Sıvı alt sensöre ulaştığında `TRUE` olur |
| `bHighLevelSensor` | `BOOL` | Giriş | Sıvı üst sensöre ulaştığında `TRUE` olur |
| `bResetAlarm` | `BOOL` | Giriş | Uygun koşulda sensör alarmını sıfırlar |
| `bInletValve` | `BOOL` | Çıkış | Dolum vanası komutu |
| `bTankFull` | `BOOL` | Çıkış | Tankın üst seviyeye ulaştığını bildirir |
| `bSensorFault` | `BOOL` | Çıkış | Tutarsız sensör durumunu kilitler |
| `bCycleEnabled` | `BOOL` | Durum | Otomatik dolum çevriminin etkinlik durumu |

Örnekte fiziksel I/O adresi kullanılmaz; değişkenler semboliktir.

## Öğrenci deneyleri

1. Üst sensörü aktif, alt sensörü pasif yaparak alarmı gözlemleyin.
2. Tank dolduktan sonra yalnızca üst sensörü pasif yapın; vananın kapalı
   kaldığını doğrulayın.
3. Alt sensörü de pasif yaparak yeni dolumun başladığını gözlemleyin.
4. Otomatik modu kapatarak vananın güvenli biçimde kapandığını doğrulayın.
5. Dolum için bir `TON` zaman aşımı alarmı ekleyin.
6. Üçüncü bir taşma sensörü ekleyerek projeyi geliştirin.

## Güvenlik ve sınırlamalar

Bu örnek gerçek bir tesisin emniyet veya taşma koruma fonksiyonu değildir.
Fiziksel sistemde kullanılmadan önce risk analizi, mekanik taşma hattı,
sertifikalı emniyet donanımı, elektriksel kilitlemeler, vana arıza analizi ve
yetkin uzman doğrulaması gerekir.

Standart PLC kodu sertifikalı emniyet PLC'sinin veya bağımsız taşma korumasının
yerine geçmez. Python simülasyonu gerçek zaman davranışını, sensör sıçramasını,
EtherCAT haberleşmesini, vana gecikmesini ve fiziksel arızaları modellemez.

## Lisans

MIT
# otomasyon-lab-20260727-tank-level-control
Alt/üst seviye sensörleri, histerezis, dolum vanası ve sensör alarmını öğreten TwinCAT 3 ve Python eğitim projesi.
