from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    company_name = models.CharField(max_length=100, verbose_name='Nazwa firmy', blank=True, null=True)
    nip = models.CharField(max_length=50, verbose_name='NIP', blank=True, null=True)
    address = models.CharField(max_length=250, verbose_name='Adres', blank=True, null=True)
    postal_code = models.CharField(max_length=20, verbose_name='Kod pocztowy', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Miasto', blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name='Kraj', blank=True, null=True)
    delivery_time = models.CharField(max_length=10, verbose_name="Czas dostawy", blank=True, null=True)
    delivery_price = models.CharField(max_length=100, verbose_name="Dostawa", blank=True, null=True)
    b2b = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profile'

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
