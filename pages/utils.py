import random
import requests
from bs4 import BeautifulSoup
from django.conf import settings

def sifre_uret(uzunluk, kucuk, buyuk, rakam, sembol):
    havuz = ""
    if kucuk: havuz += "abcdefghijklmnopqrstuvwxyz"
    if buyuk: havuz += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if rakam: havuz += "0123456789"
    if sembol: havuz += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
    if havuz:
        return "".join(random.choice(havuz) for _ in range(uzunluk))
    return None

def hava_durumu_getir(sehir):
    # API Key'i artık settings'den güvenli şekilde alıyoruz
    api_key = settings.OPENWEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'sehir': data['name'],
                'sicaklik': round(data['main']['temp']), 
                'durum': data['weather'][0]['description'].title(),
                'ikon': data['weather'][0]['icon'] 
            }, None
        else:
            return None, "Şehir bulunamadı."
    except requests.RequestException:
        return None, "Bağlantı hatası oluştu."

def kitaplari_scrapla():
    url = "http://books.toscrape.com/"
    kitaplar = []
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            kitap_kutulari = soup.find_all("article", class_="product_pod")
            
            for kitap in kitap_kutulari[:8]:
                baslik = kitap.find("h3").find("a")["title"]
                fiyat = kitap.find("p", class_="price_color").text
                resim_yarim = kitap.find("img")["src"]
                resim_tam = "http://books.toscrape.com/" + resim_yarim.replace("../", "")
                puan_sinifi = kitap.find("p", class_="star-rating")["class"][1]
                
                kitaplar.append({
                    'baslik': baslik, 
                    'fiyat': fiyat, 
                    'resim': resim_tam, 
                    'puan': puan_sinifi
                })
            return kitaplar, None
        return [], "Kaynak siteye erişilemedi."
    except Exception as e:
        return [], f"Hata: {str(e)}"