import random
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, get_object_or_404, redirect
from .models import Proje, Hakkimda
from .forms import IletisimFormu, CeviriciFormu, SifreFormu, HavaDurumuFormu # Tüm formlar burada


# -----------------------------------------------------
# ANA SAYFALAR
# -----------------------------------------------------

def home_view(request):
    projeler = Proje.objects.all().order_by('-id') # En son eklenen en başta
    context = {"projeler": projeler}
    return render(request, "home.html", context)

def detay_view(request, pk):
    tek_proje = get_object_or_404(Proje, pk=pk)
    context = {"proje": tek_proje}
    return render(request, "detay.html", context)

def hakkimda_view(request):
    hakkimda_veri = Hakkimda.objects.first() 
    return render(request, 'hakkimda.html', {'hakkimda': hakkimda_veri})

def iletisim_view(request):
    if request.method == 'POST':
        form = IletisimFormu(request.POST)
        if form.is_valid():
            form.save()
            # Başarılı mesajı göndermek için (Opsiyonel)
            return redirect('/') 
    else:
        form = IletisimFormu()

    context = {'form': form}
    return render(request, 'iletisim.html', context)


# -----------------------------------------------------
# ARAÇLAR
# -----------------------------------------------------

def cevirici_view(request):
    sonuc = None
    form = CeviriciFormu(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        sayi = form.cleaned_data['sayi']
        islem = form.cleaned_data['islem']
        
        # Matematik Mantığı
        if islem == 'c_to_f':
            hesap = (sayi * 1.8) + 32
            sonuc = f"{sayi}°C = {hesap:.2f}°F"
        # ... diğer mantıklar ...
        elif islem == 'mil_to_km':
            hesap = sayi / 0.621371
            sonuc = f"{sayi} Mil = {hesap:.2f} KM"
            
        form = CeviriciFormu(request.POST) # Formu yeniden doldurmak
    
    return render(request, 'araclar/cevirici.html', {'form': form, 'sonuc': sonuc})

def sifre_view(request):
    uretilen_sifre = ""
    form = SifreFormu(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        uzunluk = form.cleaned_data['uzunluk']
        # ... Mantık: Havuz oluşturma, random.choice ile şifre üretme ...
        # (Önceki adımda yazdığın mantığı buraya taşıyabilirsin.)
        
        havuz = ""
        if form.cleaned_data['kucuk_harf']: havuz += "abcdefghijklmnopqrstuvwxyz"
        # ... Diğer harf/rakam/sembol havuzları ...
        
        if havuz != "":
             for i in range(uzunluk):
                uretilen_sifre += random.choice(havuz)
        else:
             uretilen_sifre = "Hata: En az bir seçenek işaretlemelisiniz!"
    
    return render(request, 'araclar/sifre.html', {'form': form, 'sifre': uretilen_sifre})


def hava_durumu_view(request):
    sonuc = None
    hata = None
    form = HavaDurumuFormu(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        sehir = form.cleaned_data['sehir']
        # API anahtarını buraya gömmek yerine, onu settings.py'den çekmelisin (Güvenlik için)
        api_key = "2702ee2453553eac14cc1081ea360b0f" # Şimdilik senin keyin kalsın
        
        url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr"
        response = requests.get(url)
        
        if response.status_code == 200:
            # ... JSON veriyi işleme mantığı ...
            data = response.json()
            sonuc = {
                'sehir': data['name'],
                'sicaklik': round(data['main']['temp']), 
                'durum': data['weather'][0]['description'].title(),
                'ikon': data['weather'][0]['icon'] 
            }
        else:
            hata = "Şehir bulunamadı veya bir hata oluştu."
            
    return render(request, 'araclar/hava.html', {'form': form, 'sonuc': sonuc, 'hata': hata})


def kitap_scraper_view(request):
    kitaplar = []
    hata = None
    
    if request.method == 'POST': # Butona basıldıysa
        try:
            url = "http://books.toscrape.com/"
            response = requests.get(url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                # ... Scraping mantığı ...
                kitap_kutulari = soup.find_all("article", class_="product_pod")
                
                for kitap in kitap_kutulari:
                    # Başlık, fiyat, resim çekme mantığı
                    baslik = kitap.find("h3").find("a")["title"]
                    fiyat = kitap.find("p", class_="price_color").text
                    resim_yarim = kitap.find("img")["src"]
                    resim_tam = "http://books.toscrape.com/" + resim_yarim
                    puan = kitap.find("p", class_="star-rating")["class"][1]

                    kitaplar.append({'baslik': baslik, 'fiyat': fiyat, 'resim': resim_tam, 'puan': puan})
            else:
                hata = "Siteye erişilemedi!"
        except Exception as e:
            hata = f"Bir hata oluştu: {e}"
            
    return render(request, 'araclar/kitaplar.html', {'kitaplar': kitaplar, 'hata': hata})