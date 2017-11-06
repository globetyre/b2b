from orders.models import OrderItem
from shop.models import Product
from account.models import Profile
import datetime
from django.http import HttpResponse
from django.utils.encoding import smart_str
import csv

# ZREALIZOWANE + AKTUALIZACJA STANÓW
def set_stock(modeladmin, request, queryset):
	queryset.update(status=2)
	for obj in queryset:
		order_id = obj.id
		for item in OrderItem.objects.filter(order=order_id):
			product = item.product_id
			quantity = item.quantity
			stocks = Product.objects.filter(id=product)
			for stock in stocks:
				stockq = stock.stock
				sub = stockq - quantity
				stock_update = Product.objects.get(id=product)
				stock_update.stock = sub
				stock_update.save()
set_stock.short_description = "Zrealizowane"

# ANULOWANE
def make_canceled(modeladmin, request, queryset):
    queryset.update(status=3)
make_canceled.short_description = "Anulowane"

# EXPORT DPD
def export_dpd(modeladmin, request, queryset):
    filename = datetime.datetime.now().strftime("%Y-%m-%d")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= "dpd_' + filename + '".csv'
    writer = csv.writer(response, delimiter=';', dialect = 'excel')
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow(['firma odbiorcy', 'ulica odbiorcy', 'miasto odbiorcy', 'kod pocztowy odbiorcy', 'liczba paczek', 'waga', 'imię i nazwisko odbiorcy', 'telefon odbiorcy', 'email odbiorcy', 'zawartość', 'nr. referencyjny 1', 'przesyłka wartościowa', 'pobranie COD - kwota', 'pobranie COD - waluta', 'opony'])

    waluta = 'PLN'
    opony = '1'
    package = '4'
    weight = '14'
    description = ''
    customer_mail = ''
    customer_phone = ''

    for obj in queryset:
        writer.writerow([
            smart_str(obj.buyer.profile.company_name),
            smart_str(obj.buyer.profile.address),
            smart_str(obj.buyer.profile.city),
            smart_str(obj.buyer.profile.postal_code),
            smart_str(package),
            smart_str(weight),
            smart_str(obj.first_name),
            smart_str(customer_phone),
            smart_str(obj.email),
            smart_str(description),
            smart_str(obj.id),
            smart_str(obj.get_total_delivery_cost),
            smart_str(obj.get_total_delivery_cost),
            smart_str(waluta),
            smart_str(opony),
        ])
    return response
export_dpd.short_description = u"DPD"
