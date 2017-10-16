from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

status_choices = (('Nowe', 'Nowe'), ('Wysłane', 'Wysłane'), ('Anulowane', 'Anulowane'))

class Status(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.CharField(max_length=200, db_index=True)
    priority = models.PositiveIntegerField(verbose_name="Priorytet")

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statusy"

    def __str__(self):
        return self.name

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
	status = models.ForeignKey(Status, related_name='status', default=1)
	kurier = models.BooleanField("Wysyłka kurierem", default=False)

	class Meta:
		ordering = ('-created',)
		verbose_name = 'Zamówienie'
		verbose_name_plural = 'Zamówienia'

	def __str__(self):
		return 'Zamówienie {}'.format(self.id)

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all())

	def get_total_delivery(self):
		return sum(item.get_delivery() for item in self.items.all())

	def get_total_delivery_cost(self):
		return sum(item.get_delivery_cost() for item in self.items.all())

class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items')
	product = models.ForeignKey(Product, related_name='order_items')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)

	def __str__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity

	def get_delivery(self):
		return self.quantity * 10

	def get_delivery_cost(self):
		return (self.price * self.quantity) + (self.quantity * 10)
