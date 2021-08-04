from rest_framework.decorators import api_view, permission_classes
from teacher.serializer import *
from accountancy.serializer import AccountSerializer
from .serializer import *
# from teacher.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from djangorest.permission import Issuperuser, Isstaff, HaveData
from collections import OrderedDict
from exam.models import OkulSınav
from exam.serializer import ExamSerializer

liste = ["pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"]


# Create your views here.


@api_view(["POST"])
@permission_classes([IsAuthenticated, Issuperuser, HaveData])
def registerStudent(request):
    data = request.data
    data = dict(data)
    data.update({i: data[i][0] or None for i in data})

    serializer = StudentSerializer(data=data)
    s = AccountSerializer(data=data)
    s1 = Öğrenci.objects.using(request.user.email).filter(no=data["no"]).first()
    data["user"] = 1

    # Burası çok güzel
    if serializer.is_valid() and s.is_valid() and not s1:
        pass
    else:
        if serializer.errors:
            err = serializer.errors
        elif s.errors:
            err = s.errors
        else:
            err = {"no": ["Bu numaraya sahip bir öğrenci zaten var"]}
        return Response(err, status=status.HTTP_400_BAD_REQUEST)

    u = User(username=data["username"],
             first_name=data["isim"],
             last_name=data["soyisim"],
             email=request.user.email)

    u.set_password(data["password"])
    try:
        u.save()
        u.save(using=u.email)
    except BaseException as e:
        return Response({"success": "False", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    data["user"] = u.id
    serializer = StudentSerializer(data=data)
    s = AccountSerializer(data=data)

    if s.is_valid():
        s.save()

    if serializer.is_valid():
        serializer.save()

    token = Token.objects.create(user=u)

    return Response({"success": "true",
                     "username": u.username,
                     "user_id": u.id,
                     "no": serializer.data["no"],
                     "token": token.key,
                     "img": serializer.data["profil_foto"]
                     }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated, Isstaff])
def öğrencilerial(request, sınıf):
    if sınıf.__contains__("-"):
        sınıf, şube = sınıf.split("-")
        students = Öğrenci.objects.using(request.user.email).filter(sınıf=sınıf, şube=şube)
    else:
        students = Öğrenci.objects.using(request.user.email).filter(sınıf=sınıf)

    if not students:
        return Response({"success": False, "error": "Böyle bir sınıf yok la"},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated, Isstaff])
def öğrencial(request, no):
    student = Öğrenci.objects.using(request.user.email).filter(no=no).first()

    if student:
        serializer = StudentSerializer(student)
        data = serializer.data.copy()
        data = dict(data)
        data["username"] = student.user.username if student.user is not None else "deleted"

        return Response(data)

    return Response({"success": False, "error": "Böyle bir öğrenci yok"},
                    status=status.HTTP_404_NOT_FOUND)


# >----- Ders Programı -----<
@api_view(["GET"])
@permission_classes([IsAuthenticated, Issuperuser])
def öğrenciprogramlarınıoluştur(request):
    u = request.user
    sınıflar = []  # basically, to show in response which classes were created
    syllabuses = ÖğretmendProgramı.objects.using(u.email).all()
    ÖğrencidProgramı.objects.using(u.email).all().delete()
    for syl in syllabuses:
        t = Öğretmen.objects.using(u.email).filter(user_id=syl.user_id).first()
        syl = syl.__dict__

        for day in liste:
            syl[day] = eval(syl[day])
            for hour in syl[day]:
                studentsyl = ÖğrencidProgramı.objects.using(u.email).filter(sınıf=syl[day][hour]).first()
                if not studentsyl:
                    studentsyl = ÖğrencidProgramı(sınıf=syl[day][hour])
                    sınıflar.append(syl[day][hour])

                studentsyl2 = studentsyl.__dict__
                studenthour = {hour: {t.get_full_name(): t.ders}}

                studentsyl2[day] = eval(studentsyl2[day])
                studentsyl2[day].update(studenthour)
                ordered = OrderedDict(sorted(studentsyl2[day].items(), key=lambda x: x[0]))
                studentsyl2[day] = dict(ordered)
                studentsyl.save(using=request.user.email)

    ss = ÖğrencidProgramı.objects.using(u.email).all()
    serializer = SSyllabusSerializer(ss, many=True)
    data = serializer.data
    for i in data:
        for j in liste:
            # i["sınıf"] = int(i["sınıf"])
            # If the name of classes are in the form of "119" this statement will be used
            i[j] = eval(i[j])
    return Response({"success": True,
                     "message": "Öğrenci Ders Programları Oluşturuldu",
                     "oluşturulan sınıflar": sınıflar,
                     "data": data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dersprogramlarınıal(request, sınıf):
    s = ÖğrencidProgramı.objects.using(request.user.email).filter(sınıf=sınıf).first()
    if not s:
        return Response({"success": False, "error": "Bu sınıfa ait ders programı bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = SSyllabusSerializer(s)
    data = serializer.data
    data.update({j: eval(data[j]) for j in liste})

    return Response(data)
