from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.files import File
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import OkulSınav, ExcelForm
from teacher.models import Öğretmen
from student.models import Öğrenci
from rest_framework import status
from .serializer import ExamSerializer, ExcelFileSerializer
from djangorest.permission import *
import pandas as pd
import numpy as np
import xlrd
from django.core.files.storage import default_storage
# Create your views here.
from statistics import mean
import pickle
from django.db.models import Q


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


@api_view(["POST"])
@permission_classes([IsAuthenticated, OnlyTeacher])
def sınavlarıoluştur(request):
    u = request.user

    data = dict(request.data)
    data.update({str(i): data[i][0] for i in data})
    sınıf = data["sınıf"]
    t = Öğretmen.objects.using(u.email).filter(user=request.user).first()

    for i in data["şubeler"].split("-"):
        öğrenciler = OkulSınav.objects.using(u.email).filter(sınıf=sınıf, şube=i)
        for öğrenci in öğrenciler:
            x = öğrenci.__dict__
            n = int(data["sınav_sayısı"])
            x[t.ders] = {str(i): {"not": -1} for i in range(1, n + 1)}
            öğrenci.save()
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def excelOluştur(request, clss: str):
    şubeler = clss.split("x")
    # for i in şubeler:
    #     s, ş = i.split("-")
    #     print(s, ş)
    print(şubeler)
    u = request.user

    dff = pd.DataFrame()
    for j in şubeler:
        s, ş = j.split("-")
        print(s, ş)
        f = ExcelForm.objects.using(u.email).filter(sınıf=s, şube=ş).first()
        if f:
            f.delete()

        students = Öğrenci.objects.using(u.email).filter(sınıf=s, şube=ş).values_list("isim", "soyisim", "sınıf", "şube", "no")
        df = pd.DataFrame(students, columns=["İsim", "Soyisim", "Sınıf", "Şube", "No"])
        df["Not"] = ""
        df["Sınav"] = 1
        dff = pd.concat([dff, df])
        print(dff)

    dff.set_index("No", inplace=True)
    dff.to_excel("öğrenciler.xlsx")
    file = File(open("öğrenciler.xlsx", "rb"))
    file.name = "{}-{}.xlsx".format(11, "a")
    form = ExcelForm(file=file, sınıf=11, şube="a")
    form.save(using=u.email)

    form_serializer = ExcelFileSerializer(form)

    return Response(form_serializer.data)

    # return Response(False)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def sınavSonuçlarınıOluşturExcel(request):
    t = Öğretmen.objects.using(request.user.email).filter(user=request.user).first()
    print(t.ders)
    liste = ["matematik", "fizik", "kimya", "biyoloji", "türk_dili", "edebiyat", "sosyal", "cografya"]
    data = request.data
    print(data["exams"])

    df = pd.read_excel(data["exams"])
    for i in range(len(df)):
        result = df.iloc[i]
        exam = OkulSınav.objects.using(request.user.email).filter(user__öğrenci__no=result["No"]).first()
        exam_dict = exam.__dict__
        # print(exam_dict)

        if str(result["Sınav"]) in exam_dict["matematik"]:
            ks = str(result["Sınav"])
            ders = eval(exam_dict["matematik"])
            print(type(result["Not"]))
            if isinstance(result["Not"], np.int64):
                ders[ks] = {"not": result["Not"]}

            exam_dict[t.ders] = ders
            exam.save()

    o = OkulSınav.objects.using(request.user.email).filter(şube__in=["b", "a"], sınıf=11)

    serializer = ExamSerializer(o, many=True)
    for i in serializer.data:
        for j in liste:
            i[j] = eval(i[j])

    if not serializer.data:
        return Response({"success": False, "error": "Sınav bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)


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
    çevir = lambda veri_listesi: int(eval(veri_listesi[0])[sınav]["not"])

    # def çevir(veri_listesi):
    #     print(veri_listesi)
    #     return int(eval(veri_listesi[0])[sınav]["not"])

    # istatistikleri_hesapla(u, data["sınıf"], data["şube"], ders, sınav)
    for i in sonuçlar:
        s = OkulSınav.objects.using(u.email).filter(user_id=i).first()
        if s:
            k = s.__dict__
            sınav_notları = eval(k[ders])

            if sınav in sınav_notları:
                sınav_notları[sınav] = {"not": sonuçlar[i]}
            else:
                return Response({"success": False,
                                 "error": "Böyle bir sınav bulunmamaktadır"},
                                status=status.HTTP_400_BAD_REQUEST)

            k[ders] = sınav_notları
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
        ders_sınavları = eval(sınavlar[ders])
        ders_sınavları[sınav]["sınıf_ort"] = sum(notlar) / len(notlar)
        ders_sınavları[sınav]["okul_ort"] = sum(ts) / len(ts)
        sınavlar[ders] = ders_sınavları
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
def sınavsonuclarınıal(request, no):
    s = OkulSınav.objects.using("beskalem").filter(user__öğrenci__no=no).first()
    if not s:
        return Response({"success": False,
                         "message": "Bu öğrenciye göre sınav sonucu bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = ExamSerializer(s)
    data = dict(serializer.data)
    data.update(
        {i: eval(data[i]) for i in ['matematik', 'fizik', 'kimya', 'biyoloji', 'türk_dili', 'edebiyat', 'sosyal', 'cografya']})
    return Response(data)

# qs = OkulSınav.objects.using(u.email).values_list("şube", "fizik")
# k = OkulSınav.objects.using(u.email).filter(Q(sınıf=11) | Q(şube="a"))
