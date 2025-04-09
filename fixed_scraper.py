import time
import json
import csv
import re
import os
import urllib.parse
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

class EndlessAbroadScraper:
    def __init__(self):
        self.base_url = "https://www.endlessabroad.com.tr"
        self.universities_url = f"{self.base_url}/universiteler"
        self.output_folder = "data"
        self.images_folder = os.path.join(self.output_folder, "images")
        
        # Çıktı klasörünü oluştur
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            
        # Resimler için klasör oluştur
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)
        
        # Tarayıcı ayarları
        chrome_options = Options()
        # Görünür mod
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        
        # WebDriver'ı başlat
        print("WebDriver başlatılıyor...")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
    
    def load_all_universities(self):
        """'Daha fazla' butonuna tıklayarak tüm üniversiteleri yükler"""
        print("Üniversiteler sayfası yükleniyor...")
        self.driver.get(self.universities_url)
        print("Sayfa yüklendi, içerik bekleniyor...")
        time.sleep(10)  # Sayfanın ilk yüklenmesi için bekle
        
        # "Daha fazla" butonunun olası seçicileri
        load_more_selectors = [
            ".more-btn button", 
            ".more-btn .btn", 
            ".more-btn .btn-border-blue",
            "button.show-more",
            ".load-more",
            "button:contains('Daha Fazla')",
            "a.btn:contains('Daha Fazla')"
        ]
        
        # Mevcut kart sayısı
        current_cards = len(self.driver.find_elements(By.CSS_SELECTOR, ".school-card"))
        print(f"Başlangıç: {current_cards} üniversite kartı yüklendi.")
        
        # Daha fazla butonu tıklanabilir durumda olduğu sürece devam et
        max_clicks = 30  # Maksimum tıklama sayısı (sonsuz döngüyü önlemek için)
        clicks = 0
        
        while clicks < max_clicks:
            load_more_button = None
            
            # Olası tüm seçicileri dene
            for selector in load_more_selectors:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for button in buttons:
                        # Butonun görünür ve "daha fazla" içerdiğini kontrol et
                        if button.is_displayed() and ("daha" in button.text.lower() or "fazla" in button.text.lower() or "göster" in button.text.lower()):
                            load_more_button = button
                            break
                    if load_more_button:
                        break
                except:
                    continue
            
            # Eğer buton bulunamadıysa daha gösterecek üniversite yok demektir
            if not load_more_button:
                print("Daha fazla butonu bulunamadı, tüm üniversiteler yüklenmiş olabilir.")
                break
            
            try:
                # JavaScript ile de tıklamayı dene (bazen daha güvenilir)
                print(f"'Daha fazla' butonuna tıklanıyor ({clicks+1}. tıklama)...")
                self.driver.execute_script("arguments[0].click();", load_more_button)
                
                # Yeni içeriğin yüklenmesi için bekle
                time.sleep(5)
                
                # Yeni kart sayısını kontrol et
                new_cards = len(self.driver.find_elements(By.CSS_SELECTOR, ".school-card"))
                
                if new_cards > current_cards:
                    print(f"Yeni kartlar yüklendi: {current_cards} -> {new_cards}")
                    current_cards = new_cards
                else:
                    print("Yeni kart yüklenmedi, tüm içerik yüklenmiş olabilir.")
                    break
                
                clicks += 1
            except Exception as e:
                print(f"Tıklama hatası: {str(e)}")
                break
        
        # Sayfanın tamamen yüklenmesi için son bir bekleme
        print("Son içeriğin yüklenmesi için bekleniyor...")
        time.sleep(10)
        
        # Yüklenen toplam kart sayısını göster
        final_cards = len(self.driver.find_elements(By.CSS_SELECTOR, ".school-card"))
        print(f"Toplam {final_cards} üniversite kartı yüklendi.")
        
        return True
    
    def get_school_card_urls(self):
        """Sayfa üzerindeki üniversite kartlarından URL'leri çıkarır"""
        # Önce tüm üniversiteleri yükle
        self.load_all_universities()
        
        # BeautifulSoup ile analiz et
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        # Üniversite kartlarını bul
        school_cards = soup.select('.school-card')
        print(f"Toplam {len(school_cards)} school-card bulundu.")
        
        urls = []
        for card in school_cards:
            # Kart içindeki title linkini bul
            title_link = card.select_one('a.title')
            if title_link and title_link.has_attr('href'):
                urls.append(title_link['href'])
        
        print(f"Toplam {len(urls)} üniversite URL'si çıkarıldı.")
        
        # İlk 5 URL'yi göster
        for i, url in enumerate(urls[:5]):
            print(f"  {i+1}. {url}")
        
        return urls
    
    def download_image(self, img_url, university_name, index):
        """Üniversiteye ait resimleri indirir"""
        if not img_url.startswith('http'):
            # Eğer göreceli URL ise, tam URL'ye çevir
            img_url = self.base_url + img_url if img_url.startswith('/') else self.base_url + "/" + img_url
        
        # Üniversite adından güvenli bir dosya adı oluştur
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', university_name)
        
        # Dosya uzantısını al
        extension = os.path.splitext(img_url.split('?')[0])[1]
        if not extension:
            extension = ".jpg"  # Uzantı yoksa varsayılan jpg
        
        # Resim dosyası adı
        img_filename = f"{safe_name}_{index}{extension}"
        img_path = os.path.join(self.images_folder, img_filename)
        
        try:
            # Resmi indir
            urllib.request.urlretrieve(img_url, img_path)
            return img_path
        except Exception as e:
            print(f"Resim indirme hatası: {str(e)} - URL: {img_url}")
            return None
    
    def scrape_university_details(self, url):
        """Üniversite detay sayfasından bilgi çeker"""
        print(f"Detay sayfası yükleniyor: {url}")
        
        # URL formatını kontrol et ve düzelt
        if not url.startswith('http'):
            url = self.base_url + url
        
        self.driver.get(url)
        time.sleep(5)  # Sayfanın yüklenmesi için bekle
        
        try:
            # BeautifulSoup ile sayfayı analiz et
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Üniversite adı (Kullanıcının verdiği HTML'den alınan seçiciler)
            name = "Bilinmiyor"
            name_selectors = [
                ".slider-title .title",   # Slider başlık
                "p.title",                # Açıklama başlığı
                "h1",                     # Ana başlık
                ".center .title",         # Merkez başlık
                ".university-detail-content h1", # Detay içeriği
                "h2.university-name"     # Alternatif başlık
            ]
            
            for selector in name_selectors:
                name_element = soup.select_one(selector)
                if name_element and name_element.text.strip():
                    name = name_element.text.strip()
                    break
            
            # Üniversite konumu
            location = "Bilinmiyor"
            location_selectors = [
                ".location",          # Ana konum
                ".center .location",  # Merkez konum
                ".location-flex span" # Konum flex içindeki span
            ]
            
            for selector in location_selectors:
                location_element = soup.select_one(selector)
                if location_element and location_element.text.strip():
                    location = location_element.text.strip()
                    break
            
            # Üniversite açıklaması
            description = ""
            description_selectors = [
                ".description.clamp-text p",   # İç açıklama
                ".description p",              # Genel açıklama
                ".text-detail .description",   # Metin detay
                ".about-text"                  # Hakkında metni
            ]
            
            for selector in description_selectors:
                description_element = soup.select_one(selector)
                if description_element and description_element.text.strip():
                    description = description_element.text.strip()
                    break
            
            # Programlar
            programs = []
            program_selectors = [
                "#programs .accordion-item .accordion-header button span",  # Program akordeon başlıkları
                "#programs .accordion-item h2",                          # Program başlıkları
                ".accordion-item h2[data-subjectid] button",             # ID'li program başlıkları
                ".program-item .program-name"                            # Program öğeleri
            ]
            
            for selector in program_selectors:
                program_elements = soup.select(selector)
                if program_elements:
                    for program in program_elements:
                        text = program.text.strip()
                        if text and len(text) > 0:
                            programs.append(text)
                    break  # İlk eşleşen seçicide dur
            
            # İmkanlar
            facilities = []
            facility_elements = soup.select(".facilities-icon .icon-div .icons-text")
            for facility in facility_elements:
                text = facility.text.strip()
                if text:
                    facilities.append(text)
            
            # Şehir bilgisi
            city_info = ""
            city_selectors = [
                "#details .details-text .desc-div div",  # Ana detay
                ".details-text .desc-div",               # Detay alt div
                ".city-info",                            # Şehir bilgisi
                ".container-text"                        # Konum metni
            ]
            
            for selector in city_selectors:
                city_element = soup.select_one(selector)
                if city_element and city_element.text.strip():
                    city_info = city_element.text.strip()
                    break
            
            # Üniversite resimleri
            images = []
            image_urls = []
            
            # Slider içindeki resimler
            slider_images = soup.select(".owl-carousel-lang-detail .post-slide .post-content img")
            if slider_images:
                for i, img in enumerate(slider_images):
                    if img.get('src'):
                        image_urls.append(img.get('src'))
            
            # Diğer resimler
            if not image_urls:  # Eğer slider resimleri bulunamadıysa alternatif arama
                alt_images = soup.select(".university-detail img, .school-detail img, .university-images img")
                for img in alt_images:
                    if img.get('src'):
                        image_urls.append(img.get('src'))
                
            # Resimleri indir ve yollarını kaydet
            for i, img_url in enumerate(image_urls[:5]):  # İlk 5 resmi al
                img_path = self.download_image(img_url, name, i+1)
                if img_path:
                    images.append({
                        "url": img_url,
                        "local_path": img_path
                    })
            
            # Sonuçları döndür
            return {
                "url": url,
                "name": name,
                "location": location,
                "description": description,
                "city_info": city_info,
                "programs": programs,
                "facilities": facilities,
                "images": images
            }
            
        except Exception as e:
            print(f"Hata: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "url": url,
                "name": "Hata oluştu",
                "location": "",
                "description": "",
                "city_info": "",
                "programs": [],
                "facilities": [],
                "images": []
            }
    
    def run(self):
        """Ana çalıştırma fonksiyonu"""
        print("Endlessabroad Scraper başlatılıyor...")
        
        # Üniversite kartlarından URL'leri topla
        university_urls = self.get_school_card_urls()
        
        if not university_urls:
            print("Hiç üniversite URL'si bulunamadı!")
            return []
        
        # Her URL için detay bilgileri çek
        universities = []
        for i, url in enumerate(university_urls):
            print(f"\nÜniversite {i+1}/{len(university_urls)} işleniyor...")
            
            university_data = self.scrape_university_details(url)
            universities.append(university_data)
            
            # Her 5 üniversitede bir yedekle
            if (i+1) % 5 == 0:
                self.save_data(universities, "partial_data.json")
                print(f"{i+1} üniversite verisi kaydedildi (kısmi).")
        
        # Tüm verileri kaydet
        if universities:
            self.save_data(universities)
            print(f"Toplam {len(universities)} üniversite verisi başarıyla kaydedildi.")
        else:
            print("Hiç veri çekilemedi!")
        
        return universities
    
    def save_data(self, data, filename="universities_data.json"):
        """Verileri JSON ve CSV formatında kaydeder"""
        # JSON olarak kaydet
        json_path = os.path.join(self.output_folder, filename)
        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        
        # Sadece ana veri dosyası için CSV de oluştur
        if filename == "universities_data.json":
            # CSV formatına dönüştür
            csv_data = []
            for uni in data:
                csv_uni = uni.copy()
                
                # Resim yollarını düzenle ve JSON olarak kaydet
                if "images" in csv_uni:
                    # İlk resmin yolu
                    if csv_uni["images"] and len(csv_uni["images"]) > 0:
                        csv_uni["first_image"] = csv_uni["images"][0].get("local_path", "")
                    else:
                        csv_uni["first_image"] = ""
                    
                    # Tüm resim yolları JSON olarak
                    csv_uni["images"] = json.dumps(csv_uni["images"], ensure_ascii=False)
                
                # Listeleri stringlere dönüştür
                if "programs" in csv_uni and isinstance(csv_uni["programs"], list):
                    csv_uni["programs"] = ", ".join(csv_uni["programs"])
                if "facilities" in csv_uni and isinstance(csv_uni["facilities"], list):
                    csv_uni["facilities"] = ", ".join(csv_uni["facilities"])
                
                csv_data.append(csv_uni)
            
            # CSV kaydet
            csv_path = os.path.join(self.output_folder, "universities_data.csv")
            if csv_data:
                keys = csv_data[0].keys()
                with open(csv_path, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=keys)
                    writer.writeheader()
                    writer.writerows(csv_data)

if __name__ == "__main__":
    scraper = EndlessAbroadScraper()
    scraper.run() 