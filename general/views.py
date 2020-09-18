from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from teacher.serializer import TeacherSerializer
from .serializer import *
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from djangorest.permission import Issuperuser, Isstaff
from datetime import *
from .models import *
from teacher.models import *
from student.models import Öğrenci
from twilio.rest import Client
from django.core.files.uploadedfile import TemporaryUploadedFile

account_sid = "AC20941e58f2e5ba23d8ab26dbf26f3697"
auth_token = "0c31727cff04a3a6655ddea8e23e8e67"
client = Client(account_sid, auth_token)
liste = ["pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"]


def index(request):
    return render(request, "index.html")


# <QueryDict: {'içerik': ['bugün yeni bir deneme sınavı yapılacak']}>
# {'içerik': 'bugün yeni bir deneme sınavı yapılacak'}
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def duyuruoluştur(request):
    u = request.user
    data = dict(request.data)
    data["oluşturan"] = u.get_full_name()
    data["içerik"] = data["içerik"][0]
    data["dosya"] = data["dosya"][0]

    serializer = NoticeSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def duyurularıal(request):
    duyurular = Duyuru.objects.using(request.user.email).all().order_by("tarih")
    serializer = NoticeSerializer(duyurular, many=True)
    return Response(serializer.data)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def duyurusil(request, id):
    n = Duyuru.objects.using(request.user.email).filter(id=id).first()
    if not n:
        return Response({"success": False, "error": "Bu ID'ye Göre Duyuru Bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = NoticeSerializer(n)
    n.delete()
    return Response(serializer.data,
                    status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def dosyaları_sil(request, id):
    n = Duyuru.objects.using(request.user.email).filter(id=id).first()
    if not n or not n.dosya:
        return Response({"success": False, "error": "Bulunamadı"})
    url = n.dosya.url
    n.dosya.delete()
    return Response({"success": True, "message": str(url)+" silindi"})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mesaj_gönder(request, no, t):
    s = Öğrenci.objects.using(request.user.email).filter(no=no).first()
    if not s:
        return Response({"success": False, "error": "Böyle bir öğrenci yok"},
                        status=status.HTTP_404_NOT_FOUND)

    if t == "m":
        from_ = '+12058833188'
        to = '+9{}'.format(s.veli_tel)
    else:
        from_ = 'whatsapp:+14155238886'
        to = 'whatsapp:+9{}'.format(s.veli_tel)

    m = client.messages.create(
        from_=from_,
        body='{} isimli öğrenciniz derse katılmamıştır.'.format(s.isim + " " + s.soyisim),
        to=to
    )

    return Response({"success": True,
                     "message": "Mesaj Gitti",
                     "tel": s.veli_tel,
                     "sid": m.sid})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def özelmesajgönder(request, t):
    data = request.data
    to = data["to"]
    body = data["body"]
    if t == "m":
        from_ = '+12058833188'
        to = '+9{}'.format(to)
    else:
        from_ = 'whatsapp:+14155238886'
        to = 'whatsapp:+9{}'.format(to)

    m = client.messages.create(
        from_=from_,
        body=body,
        to=to,
    )

    return Response({"success": True,
                     "status": "Mesaj Gitti",
                     "to": to,
                     "body": body,
                     "sid": m.sid})
