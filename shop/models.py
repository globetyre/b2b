from django.db import models
from django.core.urlresolvers import reverse
from decimal import Decimal


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Kategoria'
        verbose_name_plural = 'Kategorie'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Images(models.Model):
    manufacturer = models.CharField(max_length=200, verbose_name="Producent", null=True, blank=True)
    model = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    class Meta:
        ordering = ('slug',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Zdjęcie'
        verbose_name_plural = 'Zdjęcia'

    def __str__(self):
        return self.slug


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products')
    name = models.CharField(max_length=200, db_index=True, verbose_name="Nazwa")
    slug = models.CharField(max_length=200, db_index=True, verbose_name="SAP")
    image = models.ForeignKey(Images, related_name='products_image', null=True, blank=True, verbose_name="Zdjęcie")
    description = models.TextField(blank=True, null=True, verbose_name="Opis")
    sap = models.CharField(max_length=200, unique=True, verbose_name="SAP")
    ean = models.CharField(max_length=200, verbose_name="EAN", null=True, blank=True)
    manufacturer = models.CharField(max_length=200, verbose_name="Producent", null=True, blank=True)
    model = models.CharField(max_length=200, verbose_name="Model bieżnika", null=True, blank=True)
    size = models.CharField(max_length=200, verbose_name="Rozmiar", null=True, blank=True)
    speed_index = models.CharField(max_length=200, verbose_name="Indeks Prędkości", null=True, blank=True)
    load_index = models.CharField(max_length=200, verbose_name="Indeks Nośności", null=True, blank=True)
    rolling_resistance = models.CharField(max_length=200, verbose_name="Opor Toczenia", null=True, blank=True)
    adhesion = models.CharField(max_length=200, verbose_name="Przyczepnosc na mokrym", null=True, blank=True)
    noise = models.CharField(max_length=200, verbose_name="Hałas [db]", null=True, blank=True)
    additional_marking = models.CharField(max_length=200, verbose_name="Dodatkowe oznaczenie", null=True, blank=True)
    season = models.CharField(max_length=50, verbose_name="SEZON", null=True, blank=True)
    typ = models.CharField(max_length=50, verbose_name="TYP", null=True, blank=True)
    dot = models.CharField(max_length=5, verbose_name="DOT", null=True, blank=True)
    price = models.FloatField(default=0.0, verbose_name="Netto [PL]")
    price_ue = models.FloatField(default=0.0, null=True, blank=True, verbose_name="Netto [UE]")
    stock = models.PositiveIntegerField(verbose_name="Stan")
    available = models.BooleanField(default=True, verbose_name="Dostępne")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Dodano")
    updated = models.DateTimeField(auto_now=True, verbose_name="Aktualizowano")
    sale = models.BooleanField(default=False, verbose_name="Promocja")
    search_field = models.CharField(max_length=300, verbose_name="Szukajka", null=True, blank=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Produkt'
        verbose_name_plural = 'Produkty'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])

    def brutto_pl(self):
        return round((float(self.price) * 1.23), 2)
    brutto_pl.short_description = 'Brutto [PL]'

    def brutto_eu(self):
        return round((float(self.price_ue) * 1.23), 2)
    brutto_eu.short_description = 'Brutto [EU]'
