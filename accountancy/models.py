from django.db import models

# Create your models here.


class Muhasebe(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    ilk_kayıt = models.DateField(auto_now_add=True)
    taksit = models.PositiveIntegerField()
    taksit_adedi = models.PositiveIntegerField(default=10)
    k_taksit_adedi = models.IntegerField(default=0)
    taksit_günü = models.PositiveIntegerField()
    ödenen_miktar = models.PositiveIntegerField(default=0)
    ödenecek_miktar = models.PositiveIntegerField(default=0)
    ödeme_geçmişi = models.TextField(default="{}")
    ödenmemiş_ay = models.IntegerField(null=True)
    borçlu_mu = models.BooleanField(default=False)
    tamamlandı_mı = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Muhasebeler"

    def __str__(self):
        return self.user.get_full_name()


    


