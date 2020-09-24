from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializer import *
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from djangorest.permission import Issuperuser, Isstaff, HaveData
from .models import *
from student.models import Öğrenci
from twilio.rest import Client
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
# proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})
# client = Client(account_sid, auth_token, http_client=proxy_client)

liste = ["pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"]


def index(request):
    return render(request, "index.html")


# <QueryDict: {'içerik': ['bugün yeni bir deneme sınavı yapılacak']}>
# {'içerik': 'bugün yeni bir deneme sınavı yapılacak'}
@api_view(["POST"])
@permission_classes([IsAuthenticated, Isstaff, HaveData])
def duyuruoluştur(request):
    u = request.user
    data = dict(request.data)
    for i in data:
        data[i] = data[i][0] or None
    data["oluşturan"] = u.get_full_name()

    serializer = NoticeSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def genelduyurularıal(request, to):
    duyurular = Duyuru.objects.using(request.user.email).filter(to=to).order_by("tarih")
    serializer = NoticeSerializer(duyurular, many=True)
    return Response(serializer.data)


# todo: Duyuru gönderen kişi sadece kendi duyurusunu silebilsin
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, Isstaff])
def duyurusil(request, id):
    n = Duyuru.objects.using(request.user.email).filter(id=id).first()
    if not n:
        return Response({"success": False, "error": "Bu ID'ye Göre Duyuru Bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = NoticeSerializer(n)
    n.delete()
    return Response(serializer.data,
                    status=status.HTTP_204_NO_CONTENT)


# todo: Dosyayı sadece duyuruyu gönderen kişi silebilsin
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, Isstaff])
def dosyaları_sil(request, id):
    n = Duyuru.objects.using(request.user.email).filter(id=id).first()
    if not n or not n.dosya:
        return Response({"success": False, "error": "Bulunamadı"})
    url = n.dosya.url
    n.dosya.delete()
    return Response({"success": True, "message": str(url)+" silindi"})


@api_view(["POST"])
@permission_classes([IsAuthenticated, Issuperuser])
def mesaj_gönder(request, no, t):
    client = Client(account_sid, auth_token)
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
@permission_classes([IsAuthenticated, Issuperuser, HaveData])
def özelmesajgönder(request, t):
    client = Client(account_sid, auth_token)
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
