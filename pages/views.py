import random
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages 
from .models import Proje, Hakkimda
from .forms import IletisimFormu, CeviriciFormu, SifreFormu, HavaDurumuFormu

# -----------------------------------------------------
# ANA SAYFALAR
# -----------------------------------------------------

def home_view(request):
    projeler = Proje.objects.all().order_by('-id')
    context = {"projeler": projeler}
    return render(request, "home.html", context)

def detay_view(request, pk):
    tek_proje = get_object_or_404(Proje, pk=pk)
    return render(request, "detay.html", {"proje": tek_proje})

def hakkimda_view(request):
    hakkimda_veri = Hakkimda.objects.first() 
    return render(request, 'hakkimda.html', {'hakkimda': hakkimda_veri})

def iletisim_view(request):
    if request.method == 'POST':
        form = IletisimFormu(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mesajınız başarıyla gönderildi!")
            return redirect('iletisim')
    else:
        form = IletisimFormu()
    return render(request, 'iletisim.html', {'form': form})

# -----------------------------------------------------
# ARAÇLAR (DÜZELTİLDİ VE GELİŞTİRİLDİ)
# -----------------------------------------------------

def cevirici_view(request):
    sonuc = None
    form = CeviriciFormu(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        sayi = form.cleaned_data['sayi']
        islem = form.cleaned_data['islem']
        
        # --- EKSİK OLAN MANTIKLAR EKLENDİ ---
        if islem == 'c_to_f':
            hesap = (sayi * 1.8) + 32
            sonuc = f"{sayi}°C = {hesap:.2f}°F"
            
        elif islem == 'f_to_c':
            hesap = (sayi - 32) / 1.8
            sonuc = f"{sayi}°F = {hesap:.2f}°C"
            
        elif islem == 'km_to_mil':
            hesap = sayi * 0.621371
            sonuc = f"{sayi} KM = {hesap:.2f} Mil"
            
        elif islem == 'mil_to_km':
            hesap = sayi / 0.621371
            sonuc = f"{sayi} Mil = {hesap:.2f} KM"
            
    return render(request, 'araclar/cevirici.html', {'form': form, 'sonuc': sonuc})

def sifre_view(request):
    uretilen_sifre = ""
    form = SifreFormu(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        uzunluk = form.cleaned_data['uzunluk']
        
        # --- HAVUZ MANTIĞI TAMAMLANDI ---
        havuz = ""
        if form.cleaned_data['kucuk_harf']:
            havuz += "abcdefghijklmnopqrstuvwxyz"
        if form.cleaned_data['buyuk_harf']:
            havuz += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if form.cleaned_data['rakam']:
            havuz += "0123456789"
        if form.cleaned_data['sembol']:
            havuz += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
        if havuz:
            for _ in range(uzunluk):
                uretilen_sifre += random.choice(havuz)
        else:
            uretilen_sifre = "Hata: En az bir karakter türü seçmelisiniz!"
            
    return render(request, 'araclar/sifre.html', {'form': form, 'sifre': uretilen_sifre})

def hava_durumu_view(request):
    sonuc = None
    hata = None
    form = HavaDurumuFormu(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        sehir = form.cleaned_data['sehir']
        api_key = "2702ee2453553eac14cc1081ea360b0f" # OpenWeatherMap Key
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                sonuc = {
                    'sehir': data['name'],
                    'sicaklik': round(data['main']['temp']), 
                    'durum': data['weather'][0]['description'].title(),
                    'ikon': data['weather'][0]['icon'] 
                }
            else:
                hata = "Şehir bulunamadı, lütfen yazımı kontrol edin."
        except:
            hata = "Bağlantı hatası oluştu."
            
    return render(request, 'araclar/hava.html', {'form': form, 'sonuc': sonuc, 'hata': hata})

def kitap_scraper_view(request):
    kitaplar = []
    hata = None
    
    if request.method == 'POST':
        try:
            url = "http://books.toscrape.com/"
            response = requests.get(url, timeout=10) # Timeout eklendi
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                kitap_kutulari = soup.find_all("article", class_="product_pod")
                
                # Sadece ilk 8 kitabı çekelim (Sayfa çok uzamasın)
                for kitap in kitap_kutulari[:8]:
                    baslik = kitap.find("h3").find("a")["title"]
                    fiyat = kitap.find("p", class_="price_color").text
                    
                    # Resim URL düzeltme
                    resim_yarim = kitap.find("img")["src"]
                    resim_tam = "http://books.toscrape.com/" + resim_yarim.replace("../", "") # URL düzeltmesi
                    
                    puan_sinifi = kitap.find("p", class_="star-rating")["class"][1]
                    
                    kitaplar.append({
                        'baslik': baslik, 
                        'fiyat': fiyat, 
                        'resim': resim_tam, 
                        'puan': puan_sinifi
                    })
            else:
                hata = "Kaynak siteye erişilemedi."
        except Exception as e:
            hata = f"Bir hata oluştu: {str(e)}"
            
    return render(request, 'araclar/kitaplar.html', {'kitaplar': kitaplar, 'hata': hata})