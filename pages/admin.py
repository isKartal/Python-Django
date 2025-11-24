from django.contrib import admin
from .models import Proje, Iletisim, Hakkimda

# Proje Admin Görünümü
class ProjeAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'teknoloji', 'github_url')
    search_fields = ('baslik', 'teknoloji')

# Hakkımda Admin Görünümü
class HakkimdaAdmin(admin.ModelAdmin):
    list_display = ('baslik',)
    # Kullanıcının birden fazla Hakkımda kaydı girmesini engellemek için
    def has_add_permission(self, request):
        return False if self.model.objects.count() > 0 else super().has_add_permission(request)

admin.site.register(Proje, ProjeAdmin)
admin.site.register(Iletisim)
admin.site.register(Hakkimda, HakkimdaAdmin)