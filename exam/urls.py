from django.urls import path
from .views import *

urlpatterns = [
    path('addexam', sınavlarıoluştur),
    path('rslt', sınavsonucugir),
    path('set', sınavlarıkur),
    path('res/<int:u>', sınavsonuclarınıal),

]
