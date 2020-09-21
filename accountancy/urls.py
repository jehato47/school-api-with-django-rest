from django.urls import path
from .views import *


urlpatterns = [
    # Muhasebe
    path('addacc', ödemekayıt),
    path('getpaid', ödemeal),
    path('patchacc', güncelle),
]
