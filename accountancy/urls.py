from django.urls import path
from .views import *


urlpatterns = [
    path('addacc', ödemekayıt),
    path('getpaid', ödemeal),
    path('patchacc', güncelle),
]
