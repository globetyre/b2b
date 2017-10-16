from orders.models import OrderItem
from shop.models import Product

# Wysłane
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
