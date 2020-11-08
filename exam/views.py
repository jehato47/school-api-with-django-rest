from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import OkulSınav
from teacher.models import Öğretmen
from student.models import Öğrenci
from rest_framework import status
from .serializer import ExamSerializer
from djangorest.permission import *
# Create your views here.
from statistics import mean
import pickle
from django.db.models import Q


@api_view(["POST"])
@permission_classes([IsAuthenticated, OnlyTeacher])
def sınavlarıoluştur(request):
    u = request.user
    data = dict(request.data)
    data.update({str(i): data[i][0] for i in data})
    t = Öğretmen.objects.using(u.email).filter(user=request.user).first()

    for i in data["şubeler"].split("-"):
        öğrenciler = OkulSınav.objects.using(u.email).filter(şube=i)
        for öğrenci in öğrenciler:
            x = öğrenci.__dict__
            n = int(data["sınav_sayısı"])
            x[t.ders] = {str(i): {"not": -1} for i in range(1, n + 1)}
            öğrenci.save()
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, OnlyTeacher])
def sınavsonucugir(request):
    # todo: Buradaki karmaşıklıktan kurtul
    u = request.user
    # d = Öğretmen.objects.using(u.email).values_list("ders")
    # d = set([x[0] for x in d])
    # liste = d
    liste = ["matematik", "fizik", "kimya", "biyoloji", "türk_dili", "edebiyat", "sosyal", "cografya"]
    data = request.data
    sınav = data["sınav"]
    ders = data["ders"]
    sonuçlar = data["sonuçlar"]
    çevir = lambda q: int(eval(q[0])[sınav]["not"])

    for i in sonuçlar:
        s = OkulSınav.objects.using(u.email).filter(user_id=i).first()
        if s:
            k = s.__dict__
            x = eval(k[ders])

            if sınav in x:
                x[sınav] = {"not": sonuçlar[i]}
            else:
                return Response({"success": False,
                                 "error": "Böyle bir sınav bulunmamaktadır"},
                                status=status.HTTP_400_BAD_REQUEST)
            k[ders] = x
            s.save()
    # Buraya kadar sınavları kayıt ediyor; aşağı kısım sınıf, okul ortalamalarını hesaplıyor

    # şubenin notlarını çekiyor
    şube = OkulSınav.objects.using(u.email).filter(şube=data["şube"])
    # bir sınıfın bütün şubelerinin notlarını çekiyor
    sınıf = OkulSınav.objects.using(u.email).filter(sınıf=data["sınıf"])

    # Eğer not girilmişse o notu al ve int'e çevir diyoruz
    notlar = [çevir(i) for i in şube.values_list(ders) if çevir(i) != -1]
    # Eğer sınav varsa ve not girilmişse o notu int'e çevir diyoruz
    ts = [çevir(j) for j in sınıf.values_list(ders) if j != ('{}',) and çevir(j) != -1]

    # Her bir öğrencinin sınavı için teker teker hepsini kaydet diyoruz
    for i in OkulSınav.objects.using(u.email).filter(sınıf=data["sınıf"], şube=data["şube"]):
        sınavlar = i.__dict__
        k = eval(sınavlar[ders])
        k[sınav]["sınıf_ort"] = sum(notlar) / len(notlar)
        k[sınav]["okul_ort"] = sum(ts) / len(ts)
        sınavlar[ders] = k
        i.save()

    # Burada da string jsonları normal json objesine dönüştürüyoruz
    o = OkulSınav.objects.using(u.email).filter(şube=data["şube"], sınıf=data["sınıf"])
    serializer = ExamSerializer(o, many=True)
    for i in serializer.data:
        for j in liste:
            i[j] = eval(i[j])

    if not serializer.data:
        return Response({"success": False, "error": "Sınav bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sınavlarıkur(request):
    u = request.user
    a = Öğrenci.objects.using(u.email).all()
    x = OkulSınav.objects.using(u.email).all()
    x.delete()
    for i in a:
        k = OkulSınav(user=i.user, sınıf=int(i.sınıf), şube=i.şube)
        k.save(using=u.email)

    return Response(True)


@api_view(["GET"])
def sınavsonuclarınıal(request, u):
    s = OkulSınav.objects.using("beskalem").filter(user_id=u).first()
    serializer = ExamSerializer(s)
    data = dict(serializer.data)
    data.update({i: eval(data[i]) for i in ['matematik', 'fizik', 'kimya', 'biyoloji', 'türk_dili', 'edebiyat', 'sosyal', 'cografya']})
    return Response(data)

# qs = OkulSınav.objects.using(u.email).values_list("şube", "fizik")
# k = OkulSınav.objects.using(u.email).filter(Q(sınıf=11) | Q(şube="a"))
