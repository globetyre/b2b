from django.contrib import admin
from .models import *
import csv
import datetime
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.mail import send_mail


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	raw_id_fields = ['product']

def export_to_csv(modeladmin, request, queryset):
	opts = modeladmin.model._meta
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename={}.csv'.format(opts.verbose_name)
	writer = csv.writer(response)
	fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	# Write a first row with header information
	writer.writerow([field.verbose_name for field in fields])
	# Write data rows
	for obj in queryset:
		data_row = []
		for field in fields:
			value = getattr(obj, field.name)
			if isinstance(value, datetime.datetime):
				value = value.strftime('%d/%m/%Y')
			data_row.append(value)
		writer.writerow(data_row)
	return response
export_to_csv.short_description = 'Export to CSV'

def order_detail(obj):
	return '<a href="{}"><i class="fa fa-eye" aria-hidden="true"></i></a>'.format(reverse('orders:order_detail', args=[obj.id]))
order_detail.allow_tags = True

class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'buyer', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'created', 'updated', 'tracking_number', 'status', 'invoice', order_detail]
	list_filter = ['created', 'updated', 'status']
	list_editable = [ 'status', 'tracking_number']
	inlines = [OrderItemInline]
	actions = [export_to_csv]
admin.site.register(Order, OrderAdmin)

class StatusAdmin(admin.ModelAdmin):
    list_display = ['name', 'priority']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Status, StatusAdmin)

#class DeliveryInfoAdmin(admin.ModelAdmin):
#    list_display = ['name', 'image', 'delivery_time', 'delivery_price']
#    search_fields = ['name']
#    prepopulated_fields = {'slug': ('name',)}
#admin.site.register(DeliveryInfo, DeliveryInfoAdmin)
