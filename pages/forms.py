from django import forms
from .models import Iletisim

# İletişim Formu
class IletisimFormu(forms.ModelForm):
    class Meta:
        model = Iletisim
        fields = ['isim', 'email', 'mesaj']
        widgets = {
            'isim': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız Soyadınız'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ornek@email.com'}),
            'mesaj': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Mesajınız...'}),
        }

# Birim Çevirici Seçenekleri
CEVIRME_SECENEKLERI = [
    ('c_to_f', 'Celcius ➡ Fahrenheit'),
    ('f_to_c', 'Fahrenheit ➡ Celcius'),
    ('km_to_mil', 'Kilometre ➡ Mil'),
    ('mil_to_km', 'Mil ➡ Kilometre'),
]

class CeviriciFormu(forms.Form):
    sayi = forms.FloatField(
        label="Değer", 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
    )
    islem = forms.ChoiceField(
        choices=CEVIRME_SECENEKLERI, 
        label="Dönüşüm Tipi", 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

# Şifre Oluşturucu Formu
class SifreFormu(forms.Form):
    uzunluk = forms.IntegerField(
        label="Şifre Uzunluğu", 
        min_value=4, 
        max_value=50, 
        initial=12,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    kucuk_harf = forms.BooleanField(label="Küçük Harf (a-z)", initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    buyuk_harf = forms.BooleanField(label="Büyük Harf (A-Z)", initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    rakam = forms.BooleanField(label="Rakam (0-9)", initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    sembol = forms.BooleanField(label="Sembol (!@#$)", initial=False, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

# Hava Durumu Formu
class HavaDurumuFormu(forms.Form):
    sehir = forms.CharField(
        label="Şehir", 
        max_length=50, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Örn: Istanbul, London'})
    )