from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view, permission_classes
# from django.views.decorators.csrf import csrf_protect
from .serializer import *
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from djangorest.permission import *
from .models import *
from management.models import Etüt
from management.serializer import EtudeSerializer
from datetime import *
from student.models import Öğrenci, ÖğrencidProgramı
from student.serializer import *
from twilio.rest import Client
import locale

locale.setlocale(locale.LC_ALL, 'tr_TR')

liste = ["pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"]


# IsAuthenticatedOrReadOnly kullanıcı doğrulanmışsa post request yapabilir yoksa sadece okuyabilir

# >----- Öğretmen -----<
@api_view(["POST"])
@permission_classes([IsAuthenticated, Issuperuser, HaveData])
def registerTeacher(request):
    try:
        data = request.data
        data = dict(data)
        data.update({i: data[i][0] or None for i in data})

        data["etüt_saatleri"] = str(data["etüt_saatleri"])
        serializer = TeacherSerializer(data=data, context={"request": request})
        data["user"] = 1

        if serializer.is_valid():
            pass
        else:
            return Response(serializer.errors)

        u = User(username=data["username"],
                 first_name=data["isim"],
                 last_name=data["soyisim"],
                 is_staff=True,
                 email=request.user.email)

        u.set_password(data["password"])

        u.save()
        u.save(using=u.email)
        data["user"] = u.id
        print(data)
        serializer = TeacherSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()

        token = Token.objects.create(user=u)

    except BaseException as e:
        return Response({"success": "False", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"success": "true",
                     "username": u.username,
                     "user_id": u.id,
                     "token": token.key
                     }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def öğretmenal(request, id):
    teacher = Öğretmen.objects.using(request.user.email).filter(user_id=id).first()

    if teacher:
        serializer = TeacherSerializer(teacher, context={"request": request})
        data = serializer.data.copy()
        data = dict(data)
        data["username"] = teacher.user.username
        data["kurum"] = teacher.user.email
        data["etüt_saatleri"] = eval(data["etüt_saatleri"])
        e = Etüt.objects.using(request.user.email).filter(user_id=id).first()
        if e:
            e = EtudeSerializer(e).data
            k = dict()
            k.update({item: eval(e[item]) for item in liste})
            data["etütler"] = k

        else:
            data["etütler"] = {}

        return Response(data)

    return Response({"success": False, "error": "Bulunamadı"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dersegöreöğretmenal(request, ders):
    e_date = (datetime.today() - timedelta(days=datetime.today().weekday() % 7)).date()
    t = Öğretmen.objects.using(request.user.email).filter(ders=ders)

    if not t:
        return Response({"success": False,
                         "error": ders.capitalize()+" Dersine Giren Hoca Bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = TeacherSerializer(t, many=True)
    data = serializer.data

    for i in data:
        e = Etüt.objects.using(request.user.email).filter(user_id=i["user"], date=e_date).order_by("date").last()
        if e:
            e = EtudeSerializer(e).data
            k = dict()
            k.update({item: eval(e[item]) for item in liste})
            i["etüt_saatleri"] = k
            i["date"] = e["date"]

        else:
            i["etüt_saatleri"] = {}

    return Response(data)


# >----- Ders Programı -----<
@api_view(["POST"])
@permission_classes([IsAuthenticated, Issuperuser, HaveData])
def dersprogramıekle(request):
    data = request.data
    u = request.user
    id = data["user"]
    t = Öğretmen.objects.using(u.email).filter(user_id=id).first()
    if not t:
        return Response({"success": False,
                         "error": "Böyle bir öğretmen yok la"},
                        status=status.HTTP_404_NOT_FOUND)

    data["ders"] = t.ders
    data["öğretmen"] = t.get_full_name()

    dp = ÖğretmendProgramı.objects.using(u.email).filter(user_id=id)
    if dp:
        dp.delete()

    # s = ÖğretmendProgramı(**data)
    # s.save(using=u.email)

    data.update({k: str(data[k]) for k in liste if k in data})
    serializer = TSyllabusSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        data.update({k: eval(data[k]) for k in liste if k in data})
        return Response(data)
    return Response(serializer.errors)

    # s.__dict__.pop("_state")
    # return Response(s.__dict__)


@api_view(["GET"])
@permission_classes([IsAuthenticated, Isstaff])
def dersprogramınıal(request, id):
    s = ÖğretmendProgramı.objects.using(request.user.email).filter(user_id=id).first()
    if not s:
        return Response({"success": False, "error": "Öğretmene ait ders programı bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = TSyllabusSerializer(s)
    data = serializer.data
    data.update({j: eval(data[j]) for j in liste})

    return Response(data)


@api_view(["GET"])
def derslerial(request):
    t = Öğretmen.objects.using("beskalem").all()
    dersler = [i.ders for i in t]

    return Response(set(dersler))

# u1.öğrenci_set.filter(no=132).first().sınavsonuçları


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def öğretmeningirdiğisınıflarıal(request):
    u = request.user

    dp = ÖğretmendProgramı.objects.using(u.email).filter(user=u).first()
    dp = dp.__dict__

    day = datetime.today().strftime("%A").lower()
    dp = eval(dp[day])

    dp = {dp[i]: [i] for i in dp}

    print(sorted(dp))
    return Response(dp)
