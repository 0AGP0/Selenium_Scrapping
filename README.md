# Endlessabroad Üniversite Veri Çekme Aracı

Bu proje, [Endlessabroad](https://www.endlessabroad.com.tr/) web sitesinden üniversite verilerini çekmek için geliştirilmiş bir web scraper uygulamasıdır.

## Özellikler

- Tüm üniversiteleri listeler
- Her üniversitenin detay bilgilerini çeker
- Konaklama seçeneklerini, programları ve imkanları toplar
- Verileri JSON ve CSV formatında kaydeder

## Kurulum

1. Gerekli kütüphaneleri yükleyin:
```
pip install -r requirements.txt
```

2. Programı çalıştırın:

Standart scraper (JavaScript destekli içeriği çekemez):
```
python scraper.py
```

Selenium tabanlı scraper (JavaScript destekli dinamik içeriği çekebilir):
```
python selenium_scraper.py
```

3. Sadece test etmek için:
```
python test_selenium_scraper.py
```

## Çıktı

Program çalıştırıldığında, `data` klasörü içerisinde iki dosya oluşturulur:
- `universities_data.json`: Tüm veriler JSON formatında
- `universities_data.csv`: Tüm veriler CSV formatında

Selenium scraper ayrıca aşağıdaki dosyayı da oluşturur:
- `universities_partial.json`: İşlem sırasında her 5 üniversitede bir güncellenen yedek dosya
- `page_source.html`: Sayfa kaynağının analiz için kaydedilmiş hali

## Selenium vs Standart Scraper

Bu projede iki farklı scraper bulunmaktadır:

1. **Standart Scraper (`scraper.py`)**: 
   - Basit `requests` ve `BeautifulSoup` kullanır
   - JavaScript ile yüklenen içeriği çekemez
   - Daha az bağımlılık gerektirir

2. **Selenium Scraper (`selenium_scraper.py`)**: 
   - Tarayıcı otomasyonu ile çalışır
   - JavaScript ile dinamik olarak yüklenen içeriği çekebilir
   - Daha fazla bağımlılık gerektirir (Chrome/Firefox tarayıcı ve WebDriver)
   - Sayfadaki etkileşimleri (tıklama, kaydırma vb.) gerçekleştirebilir

## Test Sonuçları ve Proje Notları

Yapılan testler sonucunda edinilen bilgiler:

1. Üniversite kartları `.school-card` CSS sınıfı ile işaretlenmiştir
2. Sayfa başına 20 üniversite kartı gösterilmektedir
3. Site JavaScript ve dinamik yükleme kullanmaktadır, bu nedenle Selenium tercih edilmelidir
4. Yaygın kullanılan CSS sınıfları:
   - `school-card`: Üniversite kartları
   - `card-icon-text`: Kart içindeki ikonlar
   - `div-border`: Kenarlık içeren elementler

## Tespit Edilen Zorluklar

1. **Dinamik İçerik**: Site içeriği dinamik olarak JavaScript ile yüklenmektedir. Bu nedenle standart `requests` ve `BeautifulSoup` yaklaşımı yetersiz kalabilir.

2. **WebDriver Kararlılığı**: Selenium WebDriver'ın yüklenmesi ve çalıştırılması bazen sorunlu olabilir, özellikle Windows sistemlerde.

3. **CSS Seçicilerin Değişkenliği**: Site güncellendikçe CSS seçiciler değişebilir, bu nedenle düzenli bakım gerekebilir.

## Sorun Giderme

Selenium ile ilgili yaygın sorunlar:

1. **WebDriver Hatası**: Chrome/Firefox WebDriver yüklenirken sorun yaşanıyorsa:
   - Tarayıcınızı güncellemeyi deneyin
   - Manuel olarak WebDriver indirin ve PATH çevresel değişkenine ekleyin
   - Selenium ve webdriver-manager'ı yeniden yükleyin

2. **Bağlantı Zaman Aşımı**: 
   - `--headless` parametresi kaldırılarak tarayıcıyı görünür modda çalıştırın
   - Zaman aşımı sürelerini artırın (`time.sleep()` ve `WebDriverWait`)

3. **Element Bulunamadı**:
   - Sayfa tamamen yüklenmeden önce elementi aramayı deniyorsanız, bekleme süresini artırın
   - CSS seçicileri doğrulayın (site yapısı değişmiş olabilir)

## Not

Bu araç sadece eğitim amaçlıdır. Web sitesinin kullanım koşullarına uygun olarak kullanılmalıdır. 