from django.urls import path
from .views import *


urlpatterns = [
    path('addteacher', registerTeacher),
    path('getteacher/<slug:id>', öğretmenal),
    path('gettbylec/<slug:ders>', dersegöreöğretmenal),
    path('addsyl', dersprogramıekle),
    path('getsyl/<int:id>', dersprogramınıal)
]
