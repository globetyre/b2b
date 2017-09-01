from django.core.mail import send_mail
from .models import Order
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives

def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Globe Tyre B2B - Zamówienie nr. {}'.format(order.id)
    from_email = 'sklep@sprzedajemyopony.pl'
    to = order.email
    text_content = 'Zamówienie złożono'
    html_content = render_to_string('orders/mail/order_created.html', {'order':order})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def order_placed(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Nowe Zamówienie nr. {}'.format(order.id)
    from_email = 'sklep@sprzedajemyopony.pl'
    to = 'sklep@sprzedajemyopony.pl'
    text_content = 'Zamówienie złożono'
    html_content = render_to_string('orders/mail/order placed.html', {'order':order})
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
