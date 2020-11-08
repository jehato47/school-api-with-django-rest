from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from student.models import Öğrenci
from management.serializer import EtudeSerializer
from student.serializer import StudentSerializer
from teacher.serializer import TeacherSerializer
from teacher.models import Öğretmen
from administrator.models import Yönetici
from administrator.serializer import YöneticiSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from djangorest.permission import Issuperuser
from datetime import *
from django.utils import timezone

liste = ["pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"]
e_date = (datetime.today() - timedelta(days=datetime.today().weekday() % 7)).date()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def userInfo(request):
    user = request.user
    try:
        if user.is_superuser:
            u = Yönetici.objects.using(user.email).filter(user_id=user.id).first()
            if u is None:
                return Response({"success": False,
                                 "error": "Siz Bir Süper Yöneticisiniz "
                                          "Lütfen Kendinize Gelin"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

            serializer = YöneticiSerializer(u)
            data = serializer.data
        elif user.is_staff:
            u = Öğretmen.objects.using(user.email).filter(user_id=user.id).first()
            serializer = TeacherSerializer(u, context={"request": request})
            data = serializer.data
            data["etüt_saatleri"] = eval(data["etüt_saatleri"])
            e = u.user.etüt_set.filter(user_id=u.user_id, date=e_date).last()
            if e:
                e = EtudeSerializer(e).data
                k = dict()
                k.update({item: eval(e[item]) for item in liste})
                data["etüt_saatleri"] = k
                data["date"] = e["date"]

        else:
            u = Öğrenci.objects.using(user.email).filter(user_id=user.id).first()
            serializer = StudentSerializer(u)
            data = serializer.data

        k = "admin" if user.is_superuser else "teacher" if user.is_staff else "student"
        data["position"] = k
        data["username"] = User.objects.using(user.email).get(id=u.user_id).username
        data["user"] = u.user_id

    except BaseException as e:
        return Response({"success": "False", "error": str(e)},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response(data, status=status.HTTP_200_OK)


@api_view(["POST"])
def loginUser(request):
    try:
        data = request.data
        u = authenticate(username=data["username"], password=data["password"])

        if not u:
            return Response({"success": False, "error": "Kullanıcı Adı veya Şifre Hatalı"},
                            status=status.HTTP_400_BAD_REQUEST)

        k = "admin" if u.is_superuser else "teacher" if u.is_staff else "student"

        u.last_login = timezone.localtime()
        u.save(update_fields=['last_login'])

        token = Token.objects.filter(user_id=u.id).first()
        if token:
            return Response({"username": u.username, "token": token.key, "position": k})

        token = Token.objects.create(user=u)
        return Response({"username": u.username, "token": token.key, "position": k})

    except BaseException as e:
        return Response({"success": "False", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    token = Token.objects.get(user_id=request.user.id)
    token.delete()
    return Response({"success": "true", "username": request.user.username})


@api_view(["GET"])
@permission_classes([IsAuthenticated, Issuperuser])
def searchuser(request):
    keyword = request.GET.get("keyword")
    öğretmenmi = int(request.GET.get("t"))
    yöneticimi = int(request.GET.get("a"))

    if yöneticimi:
        m = Yönetici.objects.using(request.user.email).filter(isim__contains=keyword)
        serializer = YöneticiSerializer(m, many=True)
        data = serializer.data
    elif öğretmenmi:
        m = Öğretmen.objects.using(request.user.email).filter(isim__contains=keyword, user__email=request.user.email)

        serializer = TeacherSerializer(m, many=True, context={"request": request})
        data = serializer.data

        for i, j in list(zip(data, m)):
            i["etüt_saatleri"] = eval(i["etüt_saatleri"])
            e = j.user.etüt_set.filter(user_id=i["user"], date=e_date).last()
            if e:
                e = EtudeSerializer(e).data
                k = dict()
                k.update({item: eval(e[item]) for item in liste})
                i["etüt_saatleri"] = k
                i["date"] = e["date"]
    else:
        m = Öğrenci.objects.using(request.user.email).filter(isim__contains=keyword)
        serializer = StudentSerializer(m, many=True)
        data = serializer.data

    for i in data:
        i["username"] = User.objects.get(id=i["user"]).username

    return Response(data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated, Issuperuser])
def deleteUser(request):
    id = request.data["user"]
    u = User.objects.filter(id=id).first()

    if u:
        u1 = User.objects.using(u.email).filter(id=id).first()
        u.delete()
        u1.delete()
        return Response({"success": True, "isim": u.first_name, "soyisim": u.last_name,
                        "user_id": id, "username": u.username}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"success": False, "error": "Böyle bir kullanıcı yok"})
