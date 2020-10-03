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
# Create your views here.
from statistics import mean
import pickle
from django.db.models import Q


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sınavlarıoluştur(request):
    data = dict(request.data)
    data.update({str(i): data[i][0] for i in data})
    t = Öğretmen.objects.using("beskalem").filter(user=request.user).first()

    for i in data["şubeler"].split("-"):
        öğrenciler = OkulSınav.objects.using("beskalem").filter(şube=i)
        for öğrenci in öğrenciler:
            x = öğrenci.__dict__
            n = int(data["sınav_sayısı"])
            x[t.ders] = {str(i): {"not": -1} for i in range(1, n + 1)}
            öğrenci.save()
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sınavsonucugir(request):
    liste = ["matematik", "fizik", "kimya", "biyoloji", "türk_dili", "edebiyat", "sosyal", "cografya"]
    data = request.data
    sınav = data["sınav"]
    ders = data["ders"]
    sonuçlar = data["sonuçlar"]
    çevir = lambda q: int(eval(q[0])[sınav]["not"])

    for i in sonuçlar:
        s = OkulSınav.objects.using("beskalem").filter(user_id=i).first()
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

    şube = OkulSınav.objects.using("beskalem").filter(şube=data["şube"])
    sınıf = OkulSınav.objects.using("beskalem").filter(sınıf=data["sınıf"])
    notlar = [çevir(i) for i in şube.values_list(ders) if çevir(i) != -1]
    ts = [çevir(j) for j in sınıf.values_list(ders) if çevir(j) != -1]

    for i in OkulSınav.objects.using("beskalem").filter(sınıf=data["sınıf"], şube=data["şube"]):
        sınavlar = i.__dict__
        k = eval(sınavlar[ders])
        k[sınav]["sınıf_ort"] = sum(notlar) / len(notlar)
        k[sınav]["okul_ort"] = sum(ts) / len(ts)
        sınavlar[ders] = k
        i.save()

    o = OkulSınav.objects.using("beskalem").filter(şube=data["şube"])
    serializer = ExamSerializer(o, many=True)
    for i in serializer.data:
        for j in liste:
            i[j] = eval(i[j])

    return Response(serializer.data)
    # return Response(True)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sınavlarıkur(request):
    a = Öğrenci.objects.using("beskalem").all()
    x = OkulSınav.objects.using("beskalem").all()
    x.delete()
    for i in a:
        k = OkulSınav(user=i.user, sınıf=int(i.sınıf), şube=i.şube)
        k.save(using="beskalem")

    return Response(True)

# qs = OkulSınav.objects.using("beskalem").values_list("şube", "fizik")
# k = OkulSınav.objects.using("beskalem").filter(Q(sınıf=11) | Q(şube="a"))
