from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from student.models import Öğrenci
from student.serializer import StudentSerializer
from teacher.serializer import TeacherSerializer
from teacher.models import Öğretmen
from administrator.models import Yönetici
from administrator.serializer import YöneticiSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from djangorest.permission import Issuperuser, Isstaff
from django.utils import timezone
import locale
locale.setlocale(locale.LC_TIME, "tr")


# Content.objects.filter(name="baby").first()  obje veya None almak için güzel yöntem
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
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

        else:
            u = Öğrenci.objects.using(user.email).filter(user_id=user.id).first()
            serializer = StudentSerializer(u)
            data = serializer.data
            data["sınavsonuçları"] = eval(data["sınavsonuçları"])

        k = "admin" if user.is_superuser else "öğretmen" if user.is_staff else "öğrenci"
        data["statü"] = k
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

        k = "admin" if u.is_superuser else "öğretmen" if u.is_staff else "öğrenci"

        token = Token.objects.filter(user_id=u.id).first()
        u.last_login = timezone.localtime()
        u.save(update_fields=['last_login'])

        if token:
            return Response({"username": u.username, "token": token.key, "statü": k})

        token = Token.objects.create(user=u)

        return Response({"username": u.username, "token": token.key, "statü": k})

    except BaseException as e:
        return Response({"success": "False", "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    token = Token.objects.get(user_id=request.user.id)
    token.delete()
    return Response({"success": "true", "username": request.user.username})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def searchuser(request):
    keyword = request.GET.get("keyword")
    öğretmenmi = int(request.GET.get("t"))
    yöneticimi = int(request.GET.get("a"))

    # u = User.objects.filter(username=data["username"]).first()
    if yöneticimi:
        m = Yönetici.objects.using(request.user.email).filter(isim__contains=keyword)
        serializer = YöneticiSerializer(m, many=True)
        data = serializer.data
    elif öğretmenmi:
        m = Öğretmen.objects.using(request.user.email).filter(isim__contains=keyword, user__email=request.user.email)
        serializer = TeacherSerializer(m, many=True, context={"request": request})
        data = serializer.data
        for i in data:
            i["etüt_saatleri"] = eval(i["etüt_saatleri"])
    else:
        m = Öğrenci.objects.using(request.user.email).filter(isim__contains=keyword)
        serializer = StudentSerializer(m, many=True)
        data = serializer.data

    # liste = []
    # for i in serializer.data:
    #     x = dict(i)
    #
    #     x["username"] = User.objects.get(id=x["user"]).username
    #     liste.append(x)

    return Response(data)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
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


# from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
# serializer = StudentSerializer(s, data=data)

# u = User.objects.filter(first_name__contains="je")
