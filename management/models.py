from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


class Etüt(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    date = models.DateField()
    öğretmen = models.CharField(max_length=20)
    ders = models.CharField(max_length=20)
    pazartesi = models.TextField(default="{}")
    salı = models.TextField(default="{}")
    çarşamba = models.TextField(default="{}")
    perşembe = models.TextField(default="{}")
    cuma = models.TextField(default="{}")
    cumartesi = models.TextField(default="{}")
    pazar = models.TextField(default="{}")

    class Meta:
        verbose_name_plural = "Etütler"

    def __str__(self):
        return self.öğretmen


class Yoklama(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    ders = models.CharField(max_length=15)
    gelenler = models.CharField(max_length=300)
    gelmeyenler = models.CharField(max_length=300)
    izinliler = models.CharField(max_length=300)
    geç_gelenler = models.CharField(max_length=300)
    sınıf = models.CharField(max_length=20, blank=False)
    öğretmen = models.CharField(max_length=30)
    derssaati = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Yoklamalar"

    def __str__(self):
        return "{} {}".format(self.ders, self.date)


def file_control(value):  # add this to some file where you can import it from
    limit = 25 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Dosya çok büyük. 25 mb tan küçük olmalı')


class Ödev(models.Model):
    ogretmen = models.CharField(max_length=30)
    teacher_image = models.TextField(null=True, blank=True)
    dosya = models.FileField(null=True, blank=True, validators=[file_control])
    ders = models.CharField(max_length=20)
    sinif = models.IntegerField()
    sube = models.CharField(max_length=10, null=True)
    baslangic_tarihi = models.DateField(auto_now_add=True)
    bitis_tarihi = models.DateField()
    baslik = models.TextField()
    icerik = models.TextField()
    aciklama = models.TextField()
    yapanlar = models.TextField(default="[]")
    yapmayanlar = models.TextField(default="[]")

    class Meta:
        verbose_name_plural = "Ödevler"

    def __str__(self):
        return self.icerik
