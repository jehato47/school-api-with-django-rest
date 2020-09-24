from django.urls import path
from .views import *


urlpatterns = [
    # Öğretmen
    path('addteacher', registerTeacher),
    path('getteacher/<slug:id>', öğretmenal),
    path('gettbylec/<slug:ders>', dersegöreöğretmenal),
    # Ders Programı
    path('addsyl', dersprogramıekle),
    path('getsyl/<slug:id>', dersprogramınıal)
]
