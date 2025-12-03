from django.test import TestCase
from django.urls import reverse
from .models import Proje, Iletisim

class ProjeModelTest(TestCase):
    def setUp(self):
        # Her testten önce çalışır: Sahte bir proje oluşturuyoruz
        self.proje = Proje.objects.create(
            baslik="Test Projesi",
            aciklama="Bu bir test açıklamasıdır.",
            teknoloji="Python, Django"
        )

    def test_model_str_metodu(self):
        # __str__ metodunun başlığı döndürüp döndürmediğini test et
        self.assertEqual(str(self.proje), "Test Projesi")

    def test_anasayfa_gorunumu(self):
        # Anasayfaya istek at (GET request)
        response = self.client.get('/')
        
        # 1. Sayfa başarılı açıldı mı? (200 OK)
        self.assertEqual(response.status_code, 200)
        
        # 2. Doğru şablon (template) kullanıldı mı?
        self.assertTemplateUsed(response, 'home.html')
        
        # 3. Eklediğimiz 'Test Projesi' sayfada görünüyor mu?
        self.assertContains(response, "Test Projesi")

class IletisimPageTest(TestCase):
    def test_iletisim_sayfasi_aciliyor_mu(self):
        # 'iletisim' ismini verdiğimiz URL'e git (reverse fonksiyonu URL adından adresi bulur)
        url = reverse('iletisim')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'iletisim.html')

    def test_iletisim_formu_gonderimi(self):
        # Forma veri gönderelim (POST işlemi)
        url = reverse('iletisim')
        data = {
            'isim': 'Test Kullanıcısı',
            'email': 'test@ornek.com',
            'mesaj': 'Bu otomatik bir test mesajıdır.'
        }
        response = self.client.post(url, data)
        
        # Form başarılı gönderildiyse bizi yönlendirmeli (302 Redirect)
        self.assertEqual(response.status_code, 302)
        
        # Veritabanına kaydedilmiş mi kontrol et
        self.assertEqual(Iletisim.objects.count(), 1)
        self.assertEqual(Iletisim.objects.first().isim, 'Test Kullanıcısı')