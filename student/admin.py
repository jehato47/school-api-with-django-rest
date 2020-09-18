from django.contrib import admin
from .models import Öğrenci
# Register your models here.


# @admin.register(Öğrenci)
# class ÖğrenciAdmin(admin.ModelAdmin):
#     list_display = ["isim", "soyisim", "email", "no", "sınıf"]
#     list_display_links = ["isim"]
#     search_fields = ["isim", "soyisim"]
#     list_filter = ["sınıf", "isim", "soyisim"]
#
#     class Meta:
#         model = Öğrenci
