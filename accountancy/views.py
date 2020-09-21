from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework import status
from .models import Muhasebe
from .serializer import AccountSerializer
import time
from datetime import date
import locale
locale.setlocale(locale.LC_TIME, "tr_TR")


# Create your views here.

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ödemekayıt(request):
    data = request.data
    s = AccountSerializer(data=data)
    if s.is_valid():
        s.save()
        return Response(s.data, status=status.HTTP_201_CREATED)
    return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ödemeal(request):
    data = request.data
    m = Muhasebe.objects.using(request.user.email).filter(user_id=data["user"]).first()
    if m is None:
        return Response({"success": False, "error": "Böyle Bir Kullanıcı Bulunmamaktadır"},
                        status=status.HTTP_404_NOT_FOUND)

    ödemeler = eval(m.ödeme_geçmişi)
    toplam_ödenen = sum(ödemeler.values())

    if m.taksit * m.taksit_adedi > toplam_ödenen:
        m.tamamlandı_mı = False
        ödemeler[time.strftime("%a, %d %b %Y %H:%M:%S")] = data["ödenen"]
        toplam_ödenen = sum(ödemeler.values())

        m.ödenen_miktar = toplam_ödenen
        m.ödeme_geçmişi = str(ödemeler)

    ay_farkı = (date.today().year - m.ilk_kayıt.year) * 12 + (date.today().month - m.ilk_kayıt.month)
    # ay_farkı = (date(2020, 11, 28).year - date.today().year)*12 + (date(2020, 11, 28).month - date.today().month)

    m.ödenmemiş_ay = ay_farkı - toplam_ödenen // m.taksit
    if m.ödenmemiş_ay < 0:
        m.ödenmemiş_ay = 0
    if toplam_ödenen < ay_farkı * m.taksit:
        m.borçlu_mu = True
        m.ödenecek_miktar = ay_farkı * m.taksit - toplam_ödenen
    else:
        m.borçlu_mu = False
        m.ödenecek_miktar = m.taksit - (m.ödenen_miktar % m.taksit)

    m.k_taksit_adedi = m.taksit_adedi - toplam_ödenen // m.taksit

    if m.k_taksit_adedi < 1:
        m.tamamlandı_mı = True
        m.k_taksit_adedi = 0
        m.ödenecek_miktar = 0
        m.save()
        s = AccountSerializer(m)
        data = s.data
        data["ödeme_geçmişi"] = eval(data["ödeme_geçmişi"])
        return Response({"success": True, "message": "Taksitlerinizin tamamını ödediniz", "data": data})

    m.save()
    serializer = AccountSerializer(m)
    data = serializer.data
    data["ödeme_geçmişi"] = eval(data["ödeme_geçmişi"])
    return Response(data)


@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def güncelle(request):
    data = request.data
    m = Muhasebe.objects.using(request.user.email).filter(user_id=data["user"]).first()

    if m is None:
        return Response({"success": False,
                         "error": "Dırırıp! Böyle bir kullanıcı yok"},
                        status=status.HTTP_404_NOT_FOUND)

    if data["ög"] != "None":
        m.ödeme_geçmişi = data["ög"]
        toplam_ödenen = sum(m.ödeme_geçmişi.values())
    else:
        toplam_ödenen = sum(eval(m.ödeme_geçmişi).values())

    m.k_taksit_adedi = m.taksit_adedi - toplam_ödenen // m.taksit
    m.ödenen_miktar = toplam_ödenen
    if m.taksit * m.taksit_adedi > toplam_ödenen:
        m.tamamlandı_mı = False
    ay_farkı = (date.today().year - m.ilk_kayıt.year) * 12 + (date.today().month - m.ilk_kayıt.month)
    # ay_farkı = (date(2020, 11, 28).year - date.today().year)*12 + (date(2020, 11, 28).month - date.today().month)

    m.ödenmemiş_ay = ay_farkı - toplam_ödenen // m.taksit
    if m.ödenmemiş_ay < 0:
        m.ödenmemiş_ay = 0
    if toplam_ödenen < ay_farkı * m.taksit:
        m.borçlu_mu = True
        m.ödenecek_miktar = ay_farkı * m.taksit - toplam_ödenen
    else:
        m.borçlu_mu = False
        m.ödenecek_miktar = m.taksit - (m.ödenen_miktar % m.taksit)

    if m.k_taksit_adedi < 1:
        m.tamamlandı_mı = True
        m.k_taksit_adedi = 0
        m.ödenecek_miktar = 0
        m.save()
        s = AccountSerializer(m)
        data = s.data
        data["ödeme_geçmişi"] = eval(data["ödeme_geçmişi"])
        return Response({"success": True, "message": "Taksitlerinizin tamamını ödediniz", "data": data})

    m.save()
    serializer = AccountSerializer(m)
    data = serializer.data
    data["ödeme_geçmişi"] = eval(data["ödeme_geçmişi"])
    return Response(data)
