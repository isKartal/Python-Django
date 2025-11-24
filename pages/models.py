from django.db import models

class Proje(models.Model):
    baslik = models.CharField(max_length=100)           # Projenin adı (Kısa metin)
    aciklama = models.TextField()                       # Detaylı açıklama (Uzun metin)
    teknoloji = models.CharField(max_length=50)         # Python, Django vs.
    # upload_to='projeler/': Resimleri media/projeler klasörüne koyar.
    resim = models.ImageField(upload_to="projeler/", blank=True)
    
    def __str__(self):
        return self.baslik  # Admin panelinde projenin adını görmek için

class Iletisim(models.Model):
    isim = models.CharField(max_length=100)
    email = models.EmailField()
    mesaj = models.TextField()
    
    def __str__(self):
        return self.email