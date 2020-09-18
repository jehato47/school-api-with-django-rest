from django.contrib import admin
from .models import Öğretmen

# Register your models here.


# @admin.register(Öğretmen)
# class ÖğretmenAdmin(admin.ModelAdmin):
#     list_display = ["isim", "soyisim", "email", "tel", "ders"]
#     list_display_links = ["isim"]
#     search_fields = ["isim", "soyisim"]
#     list_filter = ["isim"]
#
#     class Meta:
#         model = Öğretmen


# @admin.register(Yoklama)
# class YoklamaAdmin(admin.ModelAdmin):
#     list_display = ["date", "ders", "öğretmen", "gelenler", "gelmeyenler"]
#     list_display_links = ["date"]
#     search_fields = ["ders", "date", "öğretmen"]
#     list_filter = ["ders", "date", "öğretmen"]
#
#     class Meta:
#         model = Yoklama
