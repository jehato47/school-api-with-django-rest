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
        isim_soyisim = "{} {}".format(i.isim, i.soyisim)
        k = OkulSınav(isim_soyisim=isim_soyisim, sınıf=i.sınıf, şube=i.şube, no=i.no)
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
    sınıflar = clss.split("x")
    # for i in sınıflar:
    #     s, ş = i.split("-")
    #     print(s, ş)
    u = request.user
    ExcelForm.objects.using(u.email).all().delete()

    dff = pd.DataFrame()
    for j in sınıflar:
        s, ş = j.split("-")
        students = Öğrenci.objects.using(u.email).filter(sınıf=s, şube=ş).values_list("isim", "soyisim", "sınıf", "şube", "no")
        df = pd.DataFrame(students, columns=["İsim", "Soyisim", "Sınıf", "Şube", "No"])
        df["Not"] = ""
        df["Sınav"] = 1
        dff = pd.concat([dff, df])

    dff.set_index("No", inplace=True)
    dff.to_excel("öğrenciler.xlsx")
    file = File(open("öğrenciler.xlsx", "rb"))
    file.name = "{}.xlsx".format("-".join(sınıflar))
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
        exam = OkulSınav.objects.using(request.user.email).filter(no=result["No"]).first()
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


@api_view(["GET"])
def sınavsonuclarınıal(request, no):
    s = OkulSınav.objects.using("beskalem").filter(no=no).first()
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
