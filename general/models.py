from django.db import models
from django.core.exceptions import ValidationError


def file_control(value):  # add this to some file where you can import it from
    limit = 25 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Dosya çok büyük. 25 mb tan küçük olmalı')


class Duyuru(models.Model):
    oluşturan = models.CharField(max_length=30)
    içerik = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)
    to = models.CharField(max_length=10, default="666666")
    dosya = models.FileField(null=True, blank=True, validators=[file_control])

    class Meta:
        verbose_name_plural = "Duyurular"

    def __str__(self):
        return self.içerik

