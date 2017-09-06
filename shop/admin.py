from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['manufacturer', 'model', 'slug', 'image']
    search_fields = ['manufacturer', 'model']
    prepopulated_fields = {'slug': ('manufacturer', 'model',)}
admin.site.register(Images, ImagesAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['image', 'search_field', 'name', 'slug', 'ean', 'price', 'price_ue', 'stock', 'available', 'created', 'updated', 'brutto_pl', 'brutto_eu', 'sale']
    list_display_links = ["name"]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'price_ue', 'stock', 'available', 'image', 'sale']
    search_fields = ['search_field']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)
