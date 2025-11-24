from django.db import models

class Proje(models.Model):
    # Ana Proje Modeli (Portfolyoda Listelenen)
    baslik = models.CharField(max_length=100)
    aciklama = models.TextField()
    teknoloji = models.CharField(max_length=150, help_text="Örn: Python Django Bootstrap") # Filtreleme için
    resim = models.ImageField(upload_to="projeler/", blank=True)
    github_url = models.URLField(max_length=200, blank=True)
    
    def __str__(self):
        return self.baslik

class Iletisim(models.Model):
    # İletişim Formu Mesajları
    isim = models.CharField(max_length=100)
    email = models.EmailField()
    mesaj = models.TextField()
    
    def __str__(self):
        return f"Mesaj: {self.isim}"

class Hakkimda(models.Model):
    # Hakkımda Sayfası İçeriği (Sadece tek bir giriş beklenir)
    baslik = models.CharField(max_length=150)
    ozet = models.TextField()
    profil_resmi = models.ImageField(upload_to="profil/", blank=True)
    
    def __str__(self):
        return self.baslik
    
    class Meta:
        verbose_name_plural = "Hakkımda Sayfası (Sadece 1 Kayıt Girin)"