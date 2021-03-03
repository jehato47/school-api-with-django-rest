from django.db import models

# Create your models here.


class OkulSınav(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    sınıf = models.IntegerField()
    şube = models.CharField(max_length=10)
    matematik = models.TextField(null=True, blank=True, default="{}")
    fizik = models.TextField(null=True, blank=True, default="{}")
    kimya = models.TextField(null=True, blank=True, default="{}")
    biyoloji = models.TextField(null=True, blank=True, default="{}")
    türk_dili = models.TextField(null=True, blank=True, default="{}")
    edebiyat = models.TextField(null=True, blank=True, default="{}")
    sosyal = models.TextField(null=True, blank=True, default="{}")
    cografya = models.TextField(null=True, blank=True, default="{}")

    class Meta:
        verbose_name_plural = "Okul Sınavları"

    def __str__(self):
        return self.user.username


class ExcelForm(models.Model):
    file = models.FileField(verbose_name="file")
    sınıf = models.IntegerField()
    şube = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "Excel Form"

    def __str__(self):
        return self.file.name
