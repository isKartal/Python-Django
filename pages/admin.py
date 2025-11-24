from django.contrib import admin
from .models import Proje, Iletisim  # Kendi yazdığımız modelleri çağırdık

admin.site.register(Proje) # Ve panele kaydettik
admin.site.register(Iletisim) # İletişim modelini de kaydettik