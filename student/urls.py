from django.urls import path
from .views import *


urlpatterns = [
    # Öğrenci
    path('addstudent', registerStudent),
    path('class/<int:id>', öğrencilerial),
    path('student/<int:no>', öğrencial),
    # Ders Programı
    path('getsyl/<int:sınıf>', dersprogramlarınıal),
    path('upsyl', öğrenciprogramlarınıoluştur)
]
