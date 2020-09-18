from django.contrib import admin
from django.urls import path, include
# from general.admin import othersite
from .admins import beskalem, iz
from django.conf import settings
from django.conf.urls.static import static
from general.views import index
urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('beskalem/', beskalem.urls),
    path('iz/', iz.urls),
    path('user/', include("User.urls")),
    path("teacher/", include("teacher.urls")),
    path("student/", include("student.urls")),
    path("adm/", include("administrator.urls")),
    path("acc/", include("accountancy.urls")),
    path("general/", include("general.urls")),
    path("manage/", include("management.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Öğrenci(isim="jehat", soyisim="deniz", email="jehatdeniz@hotmail.com", sınıf=111, no=411)
# from rest_framework.renderers import JSONRenderer
# from rest_framework.parsers import JSONParser
# StudentSerializer(Öğrenci.objects.all(), many=True)
