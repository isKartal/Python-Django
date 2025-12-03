from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages 
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .models import Proje, Hakkimda
from .forms import IletisimFormu, CeviriciFormu, SifreFormu, HavaDurumuFormu
from .utils import sifre_uret, hava_durumu_getir, kitaplari_scrapla

# -----------------------------------------------------
# ANA SAYFALAR
# -----------------------------------------------------

def home_view(request):
    projeler = Proje.objects.all().order_by('-id')
    return render(request, "home.html", {"projeler": projeler})

def detay_view(request, pk):
    tek_proje = get_object_or_404(Proje, pk=pk)
    return render(request, "detay.html", {"proje": tek_proje})

def hakkimda_view(request):
    hakkimda_veri = Hakkimda.objects.first() 
    return render(request, 'hakkimda.html', {'hakkimda': hakkimda_veri})

def iletisim_view(request):
    form = IletisimFormu(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        kaydedilen_mesaj = form.save()
        
        # E-Posta Gönderimi
        try:
            konu = f"Portfolyodan Yeni Mesaj: {kaydedilen_mesaj.isim}"
            mesaj_icerigi = f"Gönderen: {kaydedilen_mesaj.isim} ({kaydedilen_mesaj.email})\n\nMesaj:\n{kaydedilen_mesaj.mesaj}"
            
            send_mail(
                subject=konu,
                message=mesaj_icerigi,
                from_email='sistem@portfolyo.com',
                recipient_list=['i.berkkartal@gmail.com'], # Kendi mail adresin
                fail_silently=False,
            )
            messages.success(request, "Mesajınız alındı ve mail iletildi!")
        except Exception as e:
            print(f"Mail Hatası: {e}")
            messages.warning(request, "Mesaj kaydedildi fakat bildirim maili gönderilemedi.")
            
        return redirect('iletisim')
    return render(request, 'iletisim.html', {'form': form})

# -----------------------------------------------------
# ARAÇLAR (HTMX DESTEKLİ)
# -----------------------------------------------------

def cevirici_view(request):
    sonuc = None
    form = CeviriciFormu(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        sayi = form.cleaned_data['sayi']
        islem = form.cleaned_data['islem']
        
        if islem == 'c_to_f':
            sonuc = f"{sayi}°C = {(sayi * 1.8) + 32:.2f}°F"
        elif islem == 'f_to_c':
            sonuc = f"{sayi}°F = {(sayi - 32) / 1.8:.2f}°C"
        elif islem == 'km_to_mil':
            sonuc = f"{sayi} KM = {sayi * 0.621371:.2f} Mil"
        elif islem == 'mil_to_km':
            sonuc = f"{sayi} Mil = {sayi / 0.621371:.2f} KM"
        
        # HTMX İsteği ise sadece sonucu döndür
        if request.headers.get('HX-Request'):
            return render(request, 'partials/cevirici_sonuc.html', {'sonuc': sonuc})
            
    return render(request, 'araclar/cevirici.html', {'form': form, 'sonuc': sonuc})

def sifre_view(request):
    uretilen_sifre = ""
    form = SifreFormu(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        sonuc = sifre_uret(
            form.cleaned_data['uzunluk'],
            form.cleaned_data['kucuk_harf'],
            form.cleaned_data['buyuk_harf'],
            form.cleaned_data['rakam'],
            form.cleaned_data['sembol']
        )
        uretilen_sifre = sonuc if sonuc else "Hata: Seçim yapın!"
        
        if request.headers.get('HX-Request'):
            return render(request, 'partials/sifre_sonuc.html', {'sifre': uretilen_sifre})
            
    return render(request, 'araclar/sifre.html', {'form': form, 'sifre': uretilen_sifre})

def hava_durumu_view(request):
    sonuc = None
    hata = None
    form = HavaDurumuFormu(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        sonuc, hata = hava_durumu_getir(form.cleaned_data['sehir'])
        
        if request.headers.get('HX-Request'):
            return render(request, 'partials/hava_sonuc.html', {'sonuc': sonuc, 'hata': hata})
            
    return render(request, 'araclar/hava.html', {'form': form, 'sonuc': sonuc, 'hata': hata})

def kitap_scraper_view(request):
    hata = None
    # Önce cache'e bak
    kitaplar = cache.get('kitaplar_verisi')

    if request.method == 'POST':
        # Cache'i yoksay, taze veri çek (Butona basıldı)
        kitaplar, hata = kitaplari_scrapla()
        if not hata:
            cache.set('kitaplar_verisi', kitaplar, 3600)
        
        if request.headers.get('HX-Request'):
             return render(request, 'partials/kitaplar_sonuc.html', {'kitaplar': kitaplar, 'hata': hata})
    
    return render(request, 'araclar/kitaplar.html', {'kitaplar': kitaplar, 'hata': hata})