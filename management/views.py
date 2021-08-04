from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from teacher.serializer import TeacherSerializer
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from djangorest.permission import *
from datetime import *
from .models import *
from teacher.models import *
from student.models import Öğrenci
from student.serializer import StudentSerializer

liste = ["pazartesi", "salı", "çarşamba", "perşembe", "cuma", "cumartesi", "pazar"]


# >----- Yoklama -----<
@api_view(["POST"])
@permission_classes([IsAuthenticated, Isstaff])
def yoklama(request):
    data = request.data
    data["user"] = request.user.id
    data["gelenler"] = str(data["gelenler"])
    data["gelmeyenler"] = str(data["gelmeyenler"])
    data["izinliler"] = str(data["izinliler"])
    data["geç_gelenler"] = str(data["geç_gelenler"])
    data["öğretmen"] = request.user.get_full_name()
    data["kurum"] = request.user.email

    serializer = AttendanceSerializer(data=data, context={'request': request})

    y = Yoklama.objects.using(request.user.email).filter(date=data["date"],
                                                         ders=data["ders"],
                                                         derssaati=data["derssaati"],
                                                         sınıf=data["sınıf"])
    if y:
        y.delete()

    if serializer.is_valid():
        serializer.save()

        data = serializer.data
        data["gelenler"] = eval(data["gelenler"])
        data["gelmeyenler"] = eval(data["gelmeyenler"])
        data["izinliler"] = eval(data["izinliler"])
        data["geç_gelenler"] = eval(data["geç_gelenler"])

        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated, Isstaff])
def yoklamayıal(request, d, ders, saat, sınıf):
    u = request.user
    y = Yoklama.objects.using(u.email).filter(user=u, derssaati=saat, date=d).first()

    if not y:
        return Response({"success": False,
                         "error": "Bu tarihe ve sınıfa ait ders programı bulunamadı"})

    serializer = AttendanceSerializer(y)

    data = serializer.data
    data["gelenler"] = eval(data["gelenler"])
    data["gelmeyenler"] = eval(data["gelmeyenler"])
    data["izinliler"] = eval(data["izinliler"])
    data["geç_gelenler"] = eval(data["geç_gelenler"])

    return Response(data)


# Todo : Buranın aşırı karışmasının sebebi birçok şeyi tek requestte almam
# Todo : Bu istisnai bir durum
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def yoklamayıaldetaylı(request, d, s, snf):
    u = request.user
    t = Öğretmen.objects.using(u.email).filter(user=u).first()
    if not t:
        return Response({"success": False, "message": "Böyle bir öğretmen yok"})
    # Todo : Burayı tamamla
    # print(date(d.split("-")))

    dp = ÖğretmendProgramı.objects.using(u.email).filter(user=u).first()
    dp = dp.__dict__

    day = datetime.today().strftime("%A").lower()
    dp = eval(dp[day])

    dp = {dp[i]: [i] for i in dp}

    if d != "0" or s != "0":
        # date = d.split("-")
        datee = [int(i) for i in d.split("-")]
        timee = [int(i) for i in s.split("-")]
        datee = datetime(*datee, *timee)
        sınıf = "{} {}".format(snf, s)
        snf, şb = snf.split("-")
        students = Öğrenci.objects.using(u.email).filter(sınıf=snf, şube=şb)
        sserializer = StudentSerializer(students, many=True)

        y = Yoklama.objects.using(u.email).filter(user=u, date=d, derssaati=s).first()
        if y:
            yserializer = AttendanceSerializer(y)
            y = {
                "gelenler": eval(yserializer.data["gelenler"]),
                "gelmeyenler": eval(yserializer.data["gelmeyenler"]),
                "izinliler": eval(yserializer.data["izinliler"]),
                "geç_gelenler": eval(yserializer.data["geç_gelenler"]),
            }

        else:
            y = {
                "gelenler": [],
                "gelmeyenler": [],
                "izinliler": [],
                "geç_gelenler": [],
            }
            [y["gelmeyenler"].append(i.no) for i in students]
        numaralar = []
        for i in y.values():
            numaralar.extend(i)
        print(numaralar)
        [y["gelmeyenler"].append(i.no) for i in students if not (i.no in numaralar)]
        return Response({"success": True, "sınıf": sınıf,
                         "öğrenciler": sserializer.data,
                         "dp": dp,
                         "date": datee,
                         "yoklama": y})

    else:
        now = datetime.now()
        day = now.strftime("%A").lower()
        dersprogramı = list(ÖğretmendProgramı.objects.using(u.email).filter(user=u).values(day))
        sözlük = {}

        for i in dersprogramı:
            for j in eval(i[day]):
                saat, dakika = j.split("-")

                dt = datetime(now.year, now.month, now.day, int(saat), int(dakika))
                k = dt - now

                if k.days >= 0:
                    sözlük[dt - now] = "{} {}".format(eval(i[day])[j], j)

        if len(sözlük) == 0:
            return Response({"success": False, "message": "Yakın zamanlı dersininiz bulunmamaktadır", "dp": dp})

        sınıfşubezaman = sözlük[min(sözlük)]
        sınıf, saat = sınıfşubezaman.split(" ")
        sınıf, şube = sınıf.split("-")

        students = Öğrenci.objects.using(u.email).filter(sınıf=sınıf, şube=şube)
        serializer = StudentSerializer(students, many=True)

        y = Yoklama.objects.using(u.email).filter(user=u, derssaati=saat, date=date.today()).first()

        if y:
            yserializer = AttendanceSerializer(y)
            y = {"gelenler": eval(yserializer.data["gelenler"]),
                 "gelmeyenler": eval(yserializer.data["gelmeyenler"]),
                 "izinliler": eval(yserializer.data["izinliler"]),
                 "geç_gelenler": eval(yserializer.data["geç_gelenler"]),
                 }
        else:
            y = {"gelenler": [],
                 "gelmeyenler": [],
                 "izinliler": [],
                 "geç_gelenler": [],
                 }
            [y["gelmeyenler"].append(i.no) for i in students]
        numaralar = []
        for i in y.values():
            numaralar.extend(i)
        print(numaralar)
        [y["gelmeyenler"].append(i.no) for i in students if not (i.no in numaralar)]
        return Response({"success": True, "sınıf": sınıfşubezaman,
                         "öğrenciler": serializer.data,
                         "dp": dp,
                         "date": now,
                         "yoklama": y})


@api_view(["GET"])
@permission_classes([IsAuthenticated, Issuperuser])
def yoklamalarıal(request):
    y = Yoklama.objects.using(request.user.email).all().order_by("date")
    serializer = AttendanceSerializer(y, many=True)
    data = serializer.data
    for i in data:
        i["gelenler"] = eval(i["gelenler"])
        i["gelmeyenler"] = eval(i["gelmeyenler"])
        i["izinliler"] = eval(i["izinliler"])
        i["geç_gelenler"] = eval(i["geç_gelenler"])

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def sınıfyoklamalarınıal(request, sınıf):
    y = Yoklama.objects.using(request.user.email).filter(sınıf=sınıf).order_by("date")
    serializer = AttendanceSerializer(y, many=True)
    data = serializer.data
    for i in data:
        i["gelenler"] = eval(i["gelenler"])
        i["gelmeyenler"] = eval(i["gelmeyenler"])
        i["izinliler"] = eval(i["izinliler"])
        i["geç_gelenler"] = eval(i["geç_gelenler"])

    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tümsınıflarıal(request):
    u = request.user
    sınıflar = Yoklama.objects.using(u.email).all().values("sınıf")
    sınıflar = [i["sınıf"] for i in sınıflar]

    return Response(set(sınıflar))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def enyakınyoklamayıal(request):
    u = request.user
    # Todo : Burayı tamamla
    now = datetime.now()
    day = now.strftime("%A").lower()
    dp = list(ÖğretmendProgramı.objects.using(u.email).filter(user=u).values(day))
    sözlük = {}

    for i in dp:
        for j in eval(i[day]):
            saat, dakika = j.split("-")

            dt = datetime(now.year, now.month, now.day, int(saat), int(dakika))
            k = dt - now

            if k.days >= 0:
                sözlük[dt - now] = "{} {}".format(eval(i[day])[j], j)

    if len(sözlük) == 0:
        return Response({"success": True, "message": "Yakın zamanlı dersininiz bulunmamaktadır"})

    sınıfşubezaman = sözlük[min(sözlük)]

    return Response({"success": True, "sınıf": sınıfşubezaman})


# >----- Etüt -----<
@api_view(["POST"])
@permission_classes([IsAuthenticated, Issuperuser])
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
@permission_classes([IsAuthenticated, IsAuthenticated, Issuperuser])
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
@permission_classes([IsAuthenticated])
def etütal(request, id):
    u = User.objects.using(request.user.email).filter(id=id).first()

    if not u:
        return Response({"success": False, "error": "Böyle Bir Kullanıcı Yok"},
                        status=status.HTTP_404_NOT_FOUND)

    e = u.etüt_set.all().order_by("date")
    if not e:
        err = u.first_name.capitalize() + " hocaya ait etüt bulunamadı"
        return Response({"success": False,
                         "error": err},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = EtudeSerializer(e, many=True)

    data = serializer.data
    [i.update({j: eval(i[j]) for j in liste}) for i in data]

    return Response(data)


# >----- Ödev -----<
@api_view(["POST"])
@permission_classes([IsAuthenticated, Isstaff])
def ödev_oluştur(request):
    u = request.user
    t = Öğretmen.objects.using(u.email).filter(user_id=u.id).first()
    if not t:
        return Response({"success": False, "error": "Böyle bir öğretmen yok"},
                        status=status.HTTP_404_NOT_FOUND)
    data = dict(request.data)
    data.update({i: data[i][0] or None for i in data})

    data["ders"] = t.ders
    data["ogretmen"] = u.get_full_name()
    data["teacher_image"] = t.profil_foto.url

    # todo : update_or_create metodunu kullan
    hw = Ödev.objects.using(u.email).filter(ogretmen=data["ogretmen"],
                                            ders=data["ders"],
                                            icerik=data["icerik"],
                                            baslik=data["baslik"],
                                            bitis_tarihi=data["bitis_tarihi"]).first()

    if hw:
        serializer = HomeworkSerializer(hw)
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
@permission_classes([IsAuthenticated])
def ödevleri_al(request, sınıf):
    sınıf, şube = sınıf.split("-")
    hw = Ödev.objects.using(request.user.email).filter(sinif=sınıf, sube=şube).order_by("baslangic_tarihi")
    serializer = HomeworkSerializer(hw, many=True)
    data = serializer.data
    for i in data:
        i["yapanlar"] = eval(i["yapanlar"])
        i["yapmayanlar"] = eval(i["yapmayanlar"])
    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated, Isstaff])
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
@permission_classes([IsAuthenticated, Isstaff])
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
