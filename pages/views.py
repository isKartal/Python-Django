from bs4 import BeautifulSoup
import requests
# get_object_or_404: Proje varsa getirir, yoksa "Sayfa Bulunamadı (404)" hatası verir.
from django.shortcuts import render, get_object_or_404, redirect # redirect eklendi
from .models import Proje  # 1. Modelimizi buraya çağırdık (Deponun anahtarı)
from .forms import IletisimFormu, CeviriciFormu, SifreFormu, HavaDurumuFormu
import random

def home_view(request):
    # 2. Veritabanındaki TÜM projeleri çekip bir listeye atıyoruz
    proje_listesi = Proje.objects.all()
    
    # 3. Bu listeyi bir "sözlük" içinde paketliyoruz
    context = {
        "projeler": proje_listesi
    }
    
    # 4. Paketi (context) HTML'e gönderiyoruz
    return render(request, "home.html", context)

def detay_view(request, pk):
    # Veritabanına git, ID'si (pk) gönderilen projeyi bul
    tek_proje = get_object_or_404(Proje, pk=pk)
    
    context = {
        "proje": tek_proje
    }
    return render(request, "detay.html", context)

def iletisim_view(request):
    if request.method == 'POST':
        # Kullanıcı butona bastıysa, gelen veriyi forma doldur
        form = IletisimFormu(request.POST)
        if form.is_valid(): # Veriler düzgün mü? (Email formatı vs.)
            form.save() # Veritabanına kaydet
            return redirect('/') # Ana sayfaya yönlendir (veya teşekkür sayfasına)
    else:
        # Sayfa ilk açılıyorsa boş form göster
        form = IletisimFormu()

    context = {
        'form': form
    }
    return render(request, 'iletisim.html', context)

def cevirici_view(request):
    sonuc = None
    
    if request.method == 'POST':
        form = CeviriciFormu(request.POST)
        if form.is_valid():
            sayi = form.cleaned_data['sayi']
            islem = form.cleaned_data['islem']
            
            # Senin converter.py dosrandaki mantık burada!
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
    else:
        form = CeviriciFormu()

    return render(request, 'araclar/cevirici.html', {'form': form, 'sonuc': sonuc})

def sifre_view(request):
    uretilen_sifre = ""
    form = SifreFormu(request.POST or None) # Hem GET hem POST için kısa yol
    
    if request.method == 'POST' and form.is_valid():
        uzunluk = form.cleaned_data['uzunluk']
        # Seçenekleri al
        kucuk = form.cleaned_data['kucuk_harf']
        buyuk = form.cleaned_data['buyuk_harf']
        rakam = form.cleaned_data['rakam']
        sembol = form.cleaned_data['sembol']
        
        havuz = ""
        if kucuk: havuz += "abcdefghijklmnopqrstuvwxyz"
        if buyuk: havuz += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if rakam: havuz += "0123456789"
        if sembol: havuz += "!@#$%^&*()_+"
        
        if havuz == "":
            uretilen_sifre = "Hata: En az bir seçenek işaretlemelisiniz!"
        else:
            # Havuzdan rastgele seçim yap
            for i in range(uzunluk):
                uretilen_sifre += random.choice(havuz)

    return render(request, 'araclar/sifre.html', {'form': form, 'sifre': uretilen_sifre})

def hava_durumu_view(request):
    sonuc = None
    hata = None
    
    if request.method == 'POST':
        form = HavaDurumuFormu(request.POST)
        if form.is_valid():
            sehir = form.cleaned_data['sehir']
            
            # Senin API Anahtarın
            api_key = "2702ee2453553eac14cc1081ea360b0f"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={sehir}&appid={api_key}&units=metric&lang=tr"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                sonuc = {
                    'sehir': data['name'],
                    'sicaklik': round(data['main']['temp']), # Küsuratı atıyoruz
                    'durum': data['weather'][0]['description'].title(),
                    'ikon': data['weather'][0]['icon'] # Güneşli/Bulutlu ikonu
                }
            else:
                hata = "Şehir bulunamadı! Lütfen yazımı kontrol edin."
    else:
        form = HavaDurumuFormu()

    return render(request, 'araclar/hava.html', {'form': form, 'sonuc': sonuc, 'hata': hata})

def hakkimda_view(request):
    return render(request, 'hakkimda.html')

def kitap_scraper_view(request):
    kitaplar = [] # Sonuçları burada toplayacağız
    hata = None
    
    if request.method == 'POST':
        try:
            url = "http://books.toscrape.com/"
            response = requests.get(url)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                # Sitedeki tüm kitap kutularını bul
                kitap_kutulari = soup.find_all("article", class_="product_pod")
                
                for kitap in kitap_kutulari:
                    # Başlık
                    baslik = kitap.find("h3").find("a")["title"]
                    # Fiyat
                    fiyat = kitap.find("p", class_="price_color").text
                    # Resim (Bonus: Siteden resim linkini de çekelim!)
                    resim_yarim = kitap.find("img")["src"]
                    resim_tam = "http://books.toscrape.com/" + resim_yarim
                    # Yıldız Puanı (Örn: 'Three', 'Four')
                    puan = kitap.find("p", class_="star-rating")["class"][1]
                    
                    kitaplar.append({
                        'baslik': baslik,
                        'fiyat': fiyat,
                        'resim': resim_tam,
                        'puan': puan
                    })
            else:
                hata = "Siteye erişilemedi!"
        except Exception as e:
            hata = f"Bir hata oluştu: {e}"
            
    return render(request, 'araclar/kitaplar.html', {'kitaplar': kitaplar, 'hata': hata})