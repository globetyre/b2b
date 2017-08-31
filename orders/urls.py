from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.order_create, name='order_create'),
	url(r'^order/(?P<order_id>\d+)/$', views.order_detail, name='order_detail'),
]
