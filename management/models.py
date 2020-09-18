from django.db import models

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
    date = models.DateField()
    ders = models.CharField(max_length=15)
    gelenler = models.CharField(max_length=300)
    gelmeyenler = models.CharField(max_length=300)
    sınıf = models.IntegerField(blank=False)
    öğretmen = models.CharField(max_length=30)
    dersaralığı = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Yoklamalar"

    def __str__(self):
        return "{} {}".format(self.ders, self.date)


class Ödev(models.Model):
    öğretmen = models.CharField(max_length=30)
    ders = models.CharField(max_length=20)
    sınıf = models.IntegerField()
    başlangıç_tarihi = models.DateField(auto_now_add=True)
    bitiş_tarihi = models.DateField()
    başlık = models.TextField()
    içerik = models.TextField()
    yapanlar = models.TextField(default="[]")
    yapmayanlar = models.TextField(default="[]")

    class Meta:
        verbose_name_plural = "Ödevler"

    def __str__(self):
        return self.içerik
