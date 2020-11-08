from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


def file_control(value):  # add this to some file where you can import it from
    types = ["png", "jpg", "jpeg", "img", ]
    ext = value.name.split(".")[-1]
    if not (ext in types):
        raise ValidationError('Resim dosyası gönderdiğinizden emin olun')

    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Dosya çok büyük. 5 mb tan küçük olmalı')


class Öğretmen(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    isim = models.CharField(max_length=100)
    soyisim = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    tel = models.CharField(max_length=15)
    ders = models.CharField(max_length=20)
    etüt_saatleri = models.TextField(default="{}", null=True, blank=True)
    profil_foto = models.FileField(null=True, default="default.jpg", validators=[file_control])

    class Meta:
        verbose_name_plural = "Öğretmenler"

    def get_full_name(self):
        return self.isim + " " + self.soyisim

    def __str__(self):
        return self.isim


class ÖğretmendProgramı(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
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
        verbose_name_plural = "Ders Programları"

    def __str__(self):
        return self.öğretmen


