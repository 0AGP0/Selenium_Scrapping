# Endlessabroad Üniversite Veri Çekme Aracı

Bu proje, [Endlessabroad](https://www.endlessabroad.com.tr/) web sitesinden üniversite verilerini otomatik olarak çekmek ve yapılandırılmış bir formatta kaydetmek için geliştirilmiş bir araçtır.

## Proje Özeti

Endlessabroad Türkiye'de yurt dışı eğitim danışmanlığı hizmeti veren bir platformdur. Bu proje, sitede listelenen üniversiteler hakkındaki bilgileri otomatik olarak toplar:
- Üniversite adları ve konumları
- Program detayları ve ücretler 
- Kampüs bilgileri
- Üniversite fotoğrafları

## Proje Bileşenleri

### Ana Dosyalar

- **fixed_scraper.py**: Selenium ve BeautifulSoup kullanarak üniversite verilerini çeken ana script
- **check_duplicates.py**: JSON veri dosyasındaki tekrar eden üniversite kayıtlarını tespit eden araç
- **requirements.txt**: Gerekli kütüphanelerin listesi
- **README.md**: Proje dokümantasyonu

### Veri Klasörü Yapısı

- **data/**: Ana veri klasörü
  - **universities_data.json**: Toplanan üniversite verileri (JSON formatında)
  - **universities_data.csv**: Toplanan üniversite verileri (CSV formatında)
  - **images/**: İndirilen üniversite fotoğrafları

## Kurulum ve Kullanım

### Gereksinimler

- Python 3.6 veya üzeri
- Chrome web tarayıcısı (Selenium için)
- Aşağıdaki Python kütüphaneleri:
  - requests
  - beautifulsoup4
  - lxml
  - selenium
  - webdriver-manager

### Kurulum Adımları

1. Depoyu klonlayın:
```
git clone https://github.com/0AGP0/Selenium_Scrapping.git
cd Selenium_Scrapping
```

2. Gerekli kütüphaneleri yükleyin:
```
pip install -r requirements.txt
```

### Kullanım

1. Üniversite verilerini çekmek için:
```
python fixed_scraper.py
```

2. Veri setinde tekrar eden üniversite kayıtlarını kontrol etmek için:
```
python check_duplicates.py
```

## Teknik Detaylar

### fixed_scraper.py

EndlessAbroadScraper sınıfını içerir ve şu adımları gerçekleştirir:
1. Chrome WebDriver'ı başlatır
2. Üniversiteler sayfasını açar
3. "Daha fazla göster" butonuna tıklayarak tüm üniversitelerin yüklenmesini sağlar
4. Her üniversitenin detay sayfasını ziyaret eder
5. Aşağıdaki verileri toplar:
   - Üniversite adı ve konumu
   - Ücret bilgileri
   - Kampüs detayları
   - Program bilgileri
   - Fotoğraflar
6. Verileri JSON ve CSV formatında kaydeder

### check_duplicates.py

Bu script şunları yapar:
1. JSON veri dosyasını okur
2. Üniversiteleri isim ve URL'ye göre gruplar
3. Birden fazla kaydı olan üniversiteleri tespit eder
4. Tekrar eden kayıtların detaylarını gösterir (URL ve konum bilgileri)

## Teknik Zorluklar ve Çözümler

1. **Dinamik Sayfa Yükleme**: Endlessabroad sitesi içeriği dinamik olarak JavaScript ile yüklediğinden, statik HTML çekimi yetersiz kalmaktadır. Bu nedenle Selenium WebDriver kullanılmıştır.

2. **Etkileşimli Elementler**: "Daha fazla göster" butonuna tıklama gibi etkileşimler için JavaScript executor kullanılmıştır.

3. **Değişken Sayfa Yapısı**: Farklı üniversite sayfalarının farklı yapılarda olabilmesi nedeniyle, çoklu CSS seçiciler ve esnek veri çekme stratejileri uygulanmıştır.

4. **Tekrar Eden Kayıtlar**: Aynı üniversitenin farklı kampüsleri için ayrı kayıtlar tutulduğu tespit edilmiştir. `check_duplicates.py` aracı bu durumu analiz etmek için geliştirilmiştir.

## Performans Optimizasyonları

- Yavaş yüklenen sayfalar için akıllı bekleme mekanizmaları
- Hata durumlarında otomatik yeniden deneme
- Resim indirme işlemleri için verimli dosya adlandırma sistemleri

## Bilgilendirme

Bu proje yalnızca eğitim amaçlıdır ve kişisel olmayan veri toplamak için geliştirilmiştir. Web sitesinin kullanım koşullarına uygun olarak kullanılması gerekmektedir. Sürekli çalıştırılan toplu veri çekme işlemleri, siteye aşırı yük bindirebilir. 