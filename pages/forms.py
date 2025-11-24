from django import forms
from .models import Iletisim

# ModelForm: Veritabanı modeline bakıp otomatik form oluşturan sihirli araç
class IletisimFormu(forms.ModelForm):
    class Meta:
        model = Iletisim
        fields = ['isim', 'email', 'mesaj']
        
        # Bootstrap sınıflarını (class) buraya ekliyoruz ki güzel görünsün
        widgets = {
            'isim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Adresiniz'}),
            'mesaj': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mesajınız...', 'rows': 5}),
        }

# Birim Çevirici için seçenekler
CEVIRME_SECENEKLERI = [
    ('c_to_f', 'Celcius -> Fahrenheit'),
    ('f_to_c', 'Fahrenheit -> Celcius'),
    ('km_to_mil', 'Kilometre -> Mil'),
    ('mil_to_km', 'Mil -> Kilometre'),
]

class CeviriciFormu(forms.Form):
    sayi = forms.FloatField(label="Değer Girin", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    islem = forms.ChoiceField(choices=CEVIRME_SECENEKLERI, label="Dönüşüm Tipi", widget=forms.Select(attrs={'class': 'form-select'}))

class SifreFormu(forms.Form):
    uzunluk = forms.IntegerField(
        label="Şifre Uzunluğu", 
        min_value=4, 
        max_value=50, 
        initial=12,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    # required=False: İşaretlemek zorunda değil (İsteğe bağlı)
    kucuk_harf = forms.BooleanField(label="Küçük Harf (a-z)", initial=True, required=False)
    buyuk_harf = forms.BooleanField(label="Büyük Harf (A-Z)", initial=True, required=False)
    rakam = forms.BooleanField(label="Rakam (0-9)", initial=True, required=False)
    sembol = forms.BooleanField(label="Sembol (!@#$)", initial=False, required=False)
    
class HavaDurumuFormu(forms.Form):
    sehir = forms.CharField(
        label="Şehir Adı", 
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Ankara, Berlin...'})
    )