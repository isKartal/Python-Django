import requests

def hava_durumu_sor():
    print("\n--- Hava Durumu Sorgulama ---")
    
    # 1. Senin API Anahtarın (Tırnak içine kendi key'ini yapıştır)
    api_key = "2702ee2453553eac14cc1081ea360b0f"
    
    # 2. Şehri sor
    sehir = input("Hangi şehrin havasını merak ediyorsun? (Örn: Istanbul): ")
    
    # 3. Adresi oluştur (URL)
    # Bu adres OpenWeatherMap'in kurallarına göre hazırlandı.
    url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr"
    
    # 4. İsteği gönder (İnternete bağlanıyor...)
    response = requests.get(url)
    
    # 5. Durumu kontrol et (200 = Başarılı, 404 = Şehir Bulunamadı)
    if response.status_code == 200:
        # Gelen veriyi JSON formatına (Python sözlüğüne) çevir
        data = response.json()
        
        # JSON içinden verileri cımbızla çekiyoruz
        sicaklik = data["main"]["temp"]
        durum = data["weather"][0]["description"]
        sehir_adi = data["name"]
        
        print(f"\n🌍 {sehir_adi} için Hava Durumu:")
        print(f"🌡️ Sıcaklık: {sicaklik}°C")
        print(f"☁️ Durum: {durum.title()}")
        
    elif response.status_code == 404:
        print("❌ Şehir bulunamadı! Lütfen yazımı kontrol et.")
    else:
        print(f"⚠️ Bir hata oluştu.")
        print(f"Hata Kodu: {response.status_code}") # Bize 401 mi 500 mü onu söyleyecek
        print(f"Sunucu Cevabı: {response.text}")     # Hatayla ilgili detayı basacak

# Programı çalıştır
while True:
    hava_durumu_sor()
    cikis = input("\nBaşka şehir? (e/h): ")
    if cikis.lower() == "h":
        print("Görüşmek üzere!")
        break