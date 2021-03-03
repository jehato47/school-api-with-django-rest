from django.urls import path
from .views import *


# todo: sınıf isimlerini düzenlemeye bak
urlpatterns = [
    # Öğrenci
    path('addstudent', registerStudent),
    path('class/<slug:sınıf>', öğrencilerial),
    path('student/<int:no>', öğrencial),
    # Ders Programı
    path('getsyl/<slug:sınıf>/<slug:şube>', dersprogramlarınıal),
    path('upsyl', öğrenciprogramlarınıoluştur)
]
