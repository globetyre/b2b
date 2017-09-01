from django.shortcuts import render
from .models import *
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .mail import order_created, order_placed
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from account.models import Profile

def order_create(request):
	deliveryinfo = DeliveryInfo.objects.all()
	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save(commit=False)
			order.buyer = request.user
			order.save()
			for item in cart:
				OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
			# clear the cart
			cart.clear()
			# launch asynchronous task
			order_created(order.id)
			order_placed(order.id)
#			order_created.delay(order.id)
		return render(request, 'orders/order/created.html', {'order': order})
	else:
		form = OrderCreateForm( initial={'first_name':request.user.first_name, 'last_name':request.user.last_name, 'email':request.user.email, 'address':request.user.profile.address, 'postal_code':request.user.profile.postal_code, 'city':request.user.profile.city, 'country':request.user.profile.country} )
	return render(request, 'orders/order/create.html', {'cart': cart, 'form': form, 'deliveryinfo': deliveryinfo})

@login_required
def order_detail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	return render(request, 'orders/order/detail.html', {'order': order})
