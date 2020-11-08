from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


def file_control(value):  # add this to some file where you can import it from
    types = ["png", "jpg", "jpeg", "img"]
    ext = value.name.split(".")[-1]
    if not (ext in types):
        raise ValidationError('Resim dosyası gönderdiğinizden emin olun')

    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Dosya çok büyük. 5 mb tan küçük olmalı')


class Öğrenci(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    sınıf = models.IntegerField(null=False, blank=False)
    şube = models.CharField(max_length=10, null=True)
    isim = models.CharField(max_length=100)
    soyisim = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    no = models.IntegerField(unique=True)
    tel = models.CharField(max_length=20, null=True, blank=True)
    veli_tel = models.CharField(max_length=20)
    profil_foto = models.FileField(default="default.jpg", null=True, validators=[file_control])

    class Meta:
        verbose_name_plural = "Öğrenciler"

    def __str__(self):
        return str(self.user)


class ÖğrencidProgramı(models.Model):
    date = models.DateField(auto_now_add=True)
    sınıf = models.CharField(max_length=20)
    pazartesi = models.TextField(default="{}")
    salı = models.TextField(default="{}")
    çarşamba = models.TextField(default="{}")
    perşembe = models.TextField(default="{}")
    cuma = models.TextField(default="{}")
    cumartesi = models.TextField(default="{}")
    pazar = models.TextField(default="{}")

    class Meta:
        verbose_name_plural = "Ders Programları"

    def __str__(self):
        return str(self.sınıf)
