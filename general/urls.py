from django.urls import path
from .views import *

urlpatterns = [
    # Mesaj
    path('sendnot/<int:no>/<slug:t>', mesaj_gönder),
    path('sendnot/<slug:t>', özelmesajgönder),
    # Duyuru
    path('addnot', duyuruoluştur),
    path('getnot/<slug:to>', genelduyurularıal),
    path('delnot/<int:id>', duyurusil),
    path('delfile/<int:id>', dosyaları_sil),
    # Veri Tabanı
    # path('backup', veritabanıyedekle),
    # path('getbackups', veritabanlarınıal)
]
