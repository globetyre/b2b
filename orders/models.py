from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

status_choices = (('New', 'New'), ('Accepted', 'Accepted'), ('Done', 'Done'), ('Rejected', 'Rejected'))

class Order(models.Model):
	buyer = models.ForeignKey(User, related_name='orders_buyer')
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	address = models.CharField(max_length=250)
	postal_code = models.CharField(max_length=20)
	city = models.CharField(max_length=100)
	country = models.CharField(max_length=100)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	invoice = models.FileField(upload_to='Invoices/%Y/%m/%d', blank=True)
	tracking_number = models.CharField(max_length=100, null=True, blank=True)
	status = models.CharField("Status", max_length=10, choices=status_choices, null=True, default="New")

	class Meta:
		ordering = ('-created',)
		verbose_name = 'Zamówienie'
		verbose_name_plural = 'Zamówienia'

	def __str__(self):
		return 'Order {}'.format(self.id)

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items')
	product = models.ForeignKey(Product, related_name='order_items')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity

class DeliveryInfo(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	slug = models.CharField(max_length=200, db_index=True)
	image = models.FileField(upload_to='flags/')
	delivery_time = models.CharField(max_length=100)
	delivery_price = models.DecimalField(max_digits=10, decimal_places=2)

	class Meta:
	    verbose_name = "DeliveryInfo"
	    verbose_name_plural = "DeliveryInfos"

	def __str__(self):
	    return 'DeliveryInfo {}'.format(self.name)
