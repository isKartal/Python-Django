"""
URL configuration for portfolyo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pages.views import home_view, detay_view, iletisim_view, cevirici_view, sifre_view, hava_durumu_view, hakkimda_view, kitap_scraper_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view), # 2. Tırnak içi boş ('') demek "Ana Sayfa" demektir.

    # <int:pk> demek: Buraya bir Tamsayı (int) gelecek ve adı "pk" (Primary Key/Kimlik) olacak.
    path('proje/<int:pk>/', detay_view, name='detay'),
    path('iletisim/', iletisim_view, name='iletisim'),
    path('araclar/cevirici/', cevirici_view, name='cevirici'),
    path('araclar/sifre/', sifre_view, name='sifre'),
    path('araclar/hava/', hava_durumu_view, name='hava'),
    path('hakkimda/', hakkimda_view, name='hakkimda'),
    path('araclar/kitaplar/', kitap_scraper_view, name='kitaplar'),
]

# Eğer DEBUG modundaysak (Geliştirme yapıyorsak) resimlere izin ver
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)