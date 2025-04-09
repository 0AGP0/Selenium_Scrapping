import json
from collections import Counter

# JSON dosyasını oku
with open('data/universities_data.json', 'r', encoding='utf-8') as file:
    universities = json.load(file)

# Üniversite sayısını yazdır
print(f"Toplam üniversite sayısı: {len(universities)}")

# İsimlere göre kontrol
uni_names = [uni.get('name', 'İsimsiz') for uni in universities]
name_counts = Counter(uni_names)
duplicates_by_name = {name: count for name, count in name_counts.items() if count > 1}

# URL'lere göre kontrol
uni_urls = [uni.get('url', 'URL Yok') for uni in universities]
url_counts = Counter(uni_urls)
duplicates_by_url = {url: count for url, count in url_counts.items() if count > 1}

# Sonuçları yazdır
if duplicates_by_name:
    print("\nİsme göre tekrar eden üniversiteler:")
    for name, count in duplicates_by_name.items():
        print(f"  - {name}: {count} kez")
else:
    print("\nİsme göre tekrar eden üniversite yok.")

if duplicates_by_url:
    print("\nURL'e göre tekrar eden üniversiteler:")
    for url, count in duplicates_by_url.items():
        print(f"  - {url}: {count} kez")
else:
    print("\nURL'e göre tekrar eden üniversite yok.")

# Eğer tekrar eden kayıt varsa, bunları detaylı olarak göster
if duplicates_by_name:
    print("\nTekrar eden üniversite detayları:")
    for name in duplicates_by_name:
        print(f"\n{name} için bulunan kayıtlar:")
        for uni in universities:
            if uni.get('name') == name:
                print(f"  - URL: {uni.get('url', 'URL Yok')}")
                location = uni.get('location', 'Konum Yok')
                if isinstance(location, dict):
                    location = f"{location.get('city', 'Şehir Yok')}, {location.get('country', 'Ülke Yok')}"
                print(f"  - Konum: {location}")
                print("  ---") 