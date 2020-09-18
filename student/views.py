from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Öğrenci
from teacher.serializer import *
from accountancy.serializer import AccountSerializer
from .serializer import *
from teacher.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from djangorest.permission import Issuperuser, Isstaff
from collections import OrderedDict

liste = ["pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"]


# Create your views here.


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, Issuperuser])
def registerStudent(request):
    try:
        data = request.data
        data = dict(data)
        for i in data:
            data[i] = data[i][0]

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
        u.save()
        u.save(using=u.email)

        data["user"] = u.id
        serializer = StudentSerializer(data=data)
        s = AccountSerializer(data=data)

        if s.is_valid():
            s.save()

        if serializer.is_valid():
            serializer.save()

        token = Token.objects.create(user=u)

    except BaseException as e:
        return Response({"success": "False", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"success": "true",
                     "username": u.username,
                     "user_id": u.id,
                     "no": serializer.data["no"],
                     "token": token.key,
                     "img": serializer.data["profil_foto"]
                     }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, Isstaff])
def öğrencilerial(request, id):
    students = Öğrenci.objects.using(request.user.email).filter(sınıf=id, user__email=request.user.email)
    if not students:
        return Response({"success": False, "error": "Böyle bir sınıf yok la"},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def öğrencial(request, no):
    student = Öğrenci.objects.using(request.user.email).filter(no=no).first()

    if student:
        serializer = StudentSerializer(student)
        data = serializer.data.copy()
        data = dict(data)
        data["username"] = User.objects.using(request.user.email).get(id=student.user.id).username
        # öğrenciden userı alabiliyoruz

        return Response(data)

    return Response({"success": False, "error": "Böyle bir öğrenci yok"},
                    status=status.HTTP_404_NOT_FOUND)


# >----- Ders Programı -----<
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def öğrenciprogramlarınıoluştur(request):
    u = request.user
    sınıflar = []  # basically, to show which classes was created
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
                ordered = OrderedDict(sorted(studentsyl2[day].items(), key=lambda x: float(x[0])))
                studentsyl2[day] = dict(ordered)
                studentsyl.save(using=request.user.email)

    ss = ÖğrencidProgramı.objects.using(u.email).all()
    serializer = SSyllabusSerializer(ss, many=True)
    data = serializer.data
    for i in data:
        for j in liste:
            i["sınıf"] = int(i["sınıf"])
            i[j] = eval(i[j])
    return Response({"success": True,
                     "message": "Öğrenci Ders Programları Oluşturuldu",
                     "oluşturulan sınıflar": sınıflar,
                     "data": data})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
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

# try:
#     student = Öğrenci.objects.get(no=no)
#     serializer = StudentSerializer(student)
#     return Response(serializer.data)
#
# except BaseException as e:
#     return Response({"success": "false", "error": str(e)}, status=status.HTTP_404_NOT_FOUND)
#
# Öğrenci.objects.filter(user__email="izeğitim")
