from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'nip', 'address', 'postal_code', 'city', 'country', 'delivery_time', 'delivery_price']
    list_display_links = ('company_name',)
    list_filter = ('country',)
    search_fields = ('company_name', 'nip',)
    raw_id_fields = ('user',)
admin.site.register(Profile, ProfileAdmin)
