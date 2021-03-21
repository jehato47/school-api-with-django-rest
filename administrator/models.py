from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.


def file_control(value):  # add this to some file where you can import it from
    types = ["png", "jpg", "jpeg"]
    ext = value.name.split(".")[-1]
    if not (ext in types):
        raise ValidationError('Resim dosyası gönderdiğinizden emin olun')

    limit = 5 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Dosya çok büyük. 5 mb tan küçük olmalı')


class Yönetici(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    isim = models.CharField(max_length=30)
    soyisim = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    mevki = models.CharField(max_length=30)
    profil_foto = models.FileField(null=True, default="default.jpg", validators=[file_control])
    kayıttarihi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Yöneticiler"

    def __str__(self):
        return self.isim
