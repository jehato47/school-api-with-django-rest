from django.contrib import admin
from .models import Yönetici

# Register your models here.


# @admin.register(Yönetici)
# class YöneticiAdmin(admin.ModelAdmin):
#     list_display = ["isim", "soyisim", "mevki", "email"]
#     list_display_links = ["isim"]
#     search_fields = ["isim"]
#     list_filter = ["mevki"]
#
#     class Meta:
#         model = Yönetici
