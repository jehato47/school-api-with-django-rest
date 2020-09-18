from django.db import models

# Create your models here.


class Yönetici(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    isim = models.CharField(max_length=30)
    soyisim = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    mevki = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Yöneticiler"

    def __str__(self):
        return self.isim
