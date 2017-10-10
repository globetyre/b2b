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
    list_display = ['image', 'name', 'slug', 'ean', 'price', 'stock', 'available', 'sale', 'updated']
    list_display_links = ["name"]
    list_filter = ['available', 'created', 'updated', 'sale', 'season', 'typ']
    list_editable = ['price', 'stock', 'available', 'image', 'sale']
    search_fields = ['name', 'sap', 'ean',]
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)
