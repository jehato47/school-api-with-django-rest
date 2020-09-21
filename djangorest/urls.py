from django.contrib import admin
from django.urls import path, include
from .admins import beskalem, iz
from django.conf import settings
from django.conf.urls.static import static
from general.views import index

urlpatterns = [
    # Anasayfa
    path('', index),
    # Admin
    path('admin/', admin.site.urls),
    path('beskalem/', beskalem.urls),
    path('iz/', iz.urls),
    # Api
    path('user/', include("User.urls")),
    path("teacher/", include("teacher.urls")),
    path("student/", include("student.urls")),
    path("adm/", include("administrator.urls")),
    path("acc/", include("accountancy.urls")),
    path("general/", include("general.urls")),
    path("manage/", include("management.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
