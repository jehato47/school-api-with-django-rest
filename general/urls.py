from django.urls import path
from .views import *

urlpatterns = [
    path('sendnot/<int:no>/<slug:t>', mesaj_gönder),
    path('sendnot/<slug:t>', özelmesajgönder),
    # path('addattendance', yoklama),
    # path('attendance', yoklamalarıal),
    # path('attendance/<slug:d>/<slug:ders>/<int:no>', yoklamayıal),
    # path('attendance/<int:no>', sınıfyoklamalarınıal),
    # path('addet', etütekle),
    # path('getset/<slug:id>', etütal),
    # path('updet', etütgüncelle),
    # path('upetuthours/<int:id>', etütsaatlerigüncelle),
    path('addnot', duyuruoluştur),
    path('getnot', duyurularıal),
    path('delnot/<int:id>', duyurusil),
    path('delfile/<int:id>', dosyaları_sil),

]

