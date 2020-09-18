from django.urls import path, include
from .views import *

urlpatterns = [
    path('getuserinfo', userInfo),
    path('loginuser', loginUser),
    path('logoutuser', logoutUser),
    path('deluser', deleteUser),
    path('srcuser', searchuser),

]


