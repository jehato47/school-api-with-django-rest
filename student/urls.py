from django.urls import path
from .views import *


urlpatterns = [
    # path('attendance/<slug:d>/<slug:ders>/<int:no>', yoklamayıal),
    path('addstudent', registerStudent),
    path('class/<int:id>', öğrencilerial),
    path('student/<int:no>', öğrencial),
    path('getsyl/<int:sınıf>', dersprogramlarınıal),
    path('upsyl', öğrenciprogramlarınıoluştur)
]
