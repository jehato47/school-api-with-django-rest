from django.urls import path
from .views import *

urlpatterns = [
    # Yoklama
    path('addattendance', yoklama),
    path('attendance', yoklamalarıal),
    path('attendance/<slug:d>/<slug:ders>/<int:no>', yoklamayıal),
    path('attendance/<int:no>', sınıfyoklamalarınıal),
    # Etüt
    path('addet', etütekle),
    path('getset/<slug:id>', etütal),
    path('updet', etütgüncelle),
    path('upetuthours/<int:id>', etütsaatlerigüncelle),
    # Ödev
    path('addhw', ödev_oluştur),
    path('gethw/<int:sınıf>', ödevleri_al),
    path('uphw/<int:id>', ödev_güncelle),
    path('delhw/<int:id>', ödev_sil)
]
