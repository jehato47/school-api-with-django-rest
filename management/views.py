from django.contrib.auth.models import User
# from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from teacher.serializer import TeacherSerializer
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from djangorest.permission import *
from datetime import *
from .models import *
from teacher.models import *

liste = ["pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"]


# >----- Yoklama -----<
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, Isstaff])
def yoklama(request):
    data = request.data

    data["gelenler"] = str(data["gelenler"])
    data["gelmeyenler"] = str(data["gelmeyenler"])
    data["öğretmen"] = request.user.get_full_name()
    data["kurum"] = request.user.email

    serializer = AttendanceSerializer(data=data, context={'request': request})

    y = Yoklama.objects.using(request.user.email).filter(date=data["date"],
                                                         ders=data["ders"],
                                                         dersaralığı=data["dersaralığı"],
                                                         sınıf=data["sınıf"])
    if y:
        y.delete()

    if serializer.is_valid():
        serializer.save()

        data = serializer.data
        data["gelenler"] = eval(data["gelenler"])
        data["gelmeyenler"] = eval(data["gelmeyenler"])

        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated, Isstaff])
def yoklamayıal(request, d, ders, no):

    x = date(*list(map(int, d.split("-"))))
    y = Yoklama.objects.using(request.user.email).filter(date=x, ders=ders, sınıf=no).first()
    if not y:
        return Response({"success": False,
                         "error": "Bugüne ve derse ait yoklama bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = AttendanceSerializer(y)

    data = serializer.data
    data["gelenler"] = eval(data["gelenler"])
    data["gelmeyenler"] = eval(data["gelmeyenler"])
    return Response(data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def yoklamalarıal(request):
    y = Yoklama.objects.using(request.user.email).all().order_by("date")
    serializer = AttendanceSerializer(y, many=True)
    data = serializer.data
    for i in data:
        i["gelenler"] = eval(i["gelenler"])
        i["gelmeyenler"] = eval(i["gelmeyenler"])

    return Response(data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sınıfyoklamalarınıal(request, no):
    y = Yoklama.objects.using(request.user.email).filter(sınıf=no).order_by("date")
    serializer = AttendanceSerializer(y, many=True)
    data = serializer.data
    for i in data:
        i["gelenler"] = eval(i["gelenler"])
        i["gelmeyenler"] = eval(i["gelmeyenler"])

    return Response(data)


# >----- Etüt -----<
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def etütekle(request):
    # ******
    etüt = lambda k: str({x: {} for x in k})
    e_date = (datetime.today() - timedelta(days=datetime.today().weekday() % 7)).date()
    # ******

    u = request.user
    data = request.data

    t = Öğretmen.objects.using(u.email).filter(user_id=data["user"]).first()

    if not t:
        return Response({"success": False,
                         "error": "Böyle Bir Öğretmen Yok"},
                        status=status.HTTP_404_NOT_FOUND)

    # **** if db has same etudes, they will be deleted
    all_etudes = Etüt.objects.using(request.user.email).filter(date__gte=e_date, user_id=data["user"])
    e = all_etudes.first()

    if all_etudes:
        all_etudes.delete()
    # ****

    data["date"] = e_date
    data["öğretmen"] = t.isim + " " + t.soyisim
    data["ders"] = t.ders
    data.update(eval(t.etüt_saatleri))

    # /^\ dict comprehension /^\ it will set empty json {} to all days
    data.update({item: etüt(data[item]) for item in liste})

    if e:
        for i in liste:
            a = eval(data[i])
            b = eval(e.__dict__[i])

            for j in a.keys():
                if j in b:
                    a[j] = b[j]
                    data[i] = str(a)

    serializer = EtudeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # ***
        data = serializer.data
        data.update({j: eval(data[j]) for j in liste})
        # ***
        return Response(data)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def etütgüncelle(request):
    e_date = (datetime.today() - timedelta(days=datetime.today().weekday() % 7)).date()
    data = request.data
    id = data["user_id"]
    gün = data["gün"]
    u = User.objects.using(request.user.email).filter(id=id).first()

    if not u:
        return Response({"success": False, "error": "Böyle Bir Kullanıcı Yok"},
                        status=status.HTTP_404_NOT_FOUND)

    t = u.öğretmen_set.all().first()
    if not t:
        return Response({"success": False, "error": "Böyle Bir Öğretmen Yok"},
                        status=status.HTTP_404_NOT_FOUND)

    e = u.etüt_set.filter(date=e_date).first()
    if not e:
        err = t.isim.capitalize() + " Hocanın Bu Haftaya Ait Etüt Verisi Yok"
        return Response({"success": False, "error": err},
                        status=status.HTTP_404_NOT_FOUND)

    o = eval(e.__dict__[gün])
    g = data["etüt"]
    x = list(set(o).difference(g).union(set(o).intersection(g)))
    x.sort(key=int)

    y = {k: (data["etüt"][k] if k in list(data["etüt"]) else o[k]) for k in x}

    d = e.__dict__
    d[gün] = y

    e.save()
    serializer = EtudeSerializer(e)
    data = serializer.data
    data.update({j: eval(data[j]) for j in liste})

    return Response(data)


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def etütsaatlerigüncelle(request, id):
    data = request.data

    t = Öğretmen.objects.using(request.user.email).filter(user_id=id).first()
    if not t:
        return Response({"success": False, "error": "Böyle Bir Öğretmen Yok"},
                        status=status.HTTP_404_NOT_FOUND)
    t.etüt_saatleri = data
    t.save()

    serializer = TeacherSerializer(t, context={"request": request})
    data = serializer.data
    data["etüt_saatleri"] = eval(data["etüt_saatleri"])
    return Response(data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def etütal(request, id):
    u = User.objects.using(request.user.email).filter(id=id).first()

    if not u:
        return Response({"success": False, "error": "Böyle Bir Kullanıcı Yok"},
                        status=status.HTTP_404_NOT_FOUND)

    e = u.etüt_set.all().order_by("date")
    if not e:
        err = u.first_name.capitalize()+" hocaya ait etüt bulunamadı"
        return Response({"success": False,
                         "error": err},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = EtudeSerializer(e, many=True)

    data = serializer.data
    [i.update({j: eval(i[j]) for j in liste}) for i in data]

    return Response(data)


# >----- Ödev -----<
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([HaveData, IsAuthenticated, Isstaff])
def ödev_oluştur(request):
    u = request.user
    t = Öğretmen.objects.using(u.email).filter(user_id=u.id).first()
    if not t:
        return Response({"success": False, "error": "Böyle bir öğretmen yok"},
                        status=status.HTTP_404_NOT_FOUND)
    data = request.data
    data["ders"] = t.ders
    data["öğretmen"] = u.get_full_name()

    hw = Ödev.objects.using(u.email).filter(öğretmen=data["öğretmen"],
                                            ders=data["ders"],
                                            içerik=data["içerik"],
                                            başlık=data["başlık"],
                                            bitiş_tarihi=data["bitiş_tarihi"]).first()

    serializer = HomeworkSerializer(hw)
    if hw:
        data = serializer.data
        data["yapanlar"] = eval(data["yapanlar"])
        data["yapmayanlar"] = eval(data["yapmayanlar"])
        return Response(data)

    serializer = HomeworkSerializer(data=data, context={"request": request})
    if serializer.is_valid():
        serializer.save()
        data = serializer.data
        data["yapanlar"] = eval(data["yapanlar"])
        data["yapmayanlar"] = eval(data["yapmayanlar"])
        return Response(data)

    else:
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ödevleri_al(request, sınıf):
    hw = Ödev.objects.using(request.user.email).filter(sınıf=sınıf).order_by("başlangıç_tarihi")
    serializer = HomeworkSerializer(hw, many=True)
    data = serializer.data
    for i in data:
        i["yapanlar"] = eval(i["yapanlar"])
        i["yapmayanlar"] = eval(i["yapmayanlar"])
    return Response(serializer.data)


@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ödev_güncelle(request, id):
    data = request.data
    hw = Ödev.objects.using(request.user.email).filter(id=id).first()
    if not hw:
        return Response({"success": False, "error": "Bu ID'ye Göre Ödev Bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)

    hw.yapanlar = data["yapanlar"]
    hw.yapmayanlar = data["yapmayanlar"]

    hw.save(update_fields=["yapanlar", "yapmayanlar"])

    serializer = HomeworkSerializer(hw)
    data = serializer.data
    data["yapanlar"] = eval(data["yapanlar"])
    data["yapmayanlar"] = eval(data["yapmayanlar"])
    return Response(data)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ödev_sil(request, id):
    hw = Ödev.objects.using(request.user.email).filter(id=id).first()

    if not hw:
        return Response({"success": False, "error": "Bu ID'ye Göre Ödev Bulunamadı"},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = HomeworkSerializer(hw)
    data = serializer.data
    data["yapanlar"] = eval(data["yapanlar"])
    data["yapmayanlar"] = eval(data["yapmayanlar"])
    hw.delete()
    return Response(data,
                    status=status.HTTP_204_NO_CONTENT)
