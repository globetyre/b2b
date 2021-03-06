from django.conf.urls import url
from . import views
from . views import *

urlpatterns = [
	url(r'^$', views.product_list, name='product_list'),
#	url(r'^jsonlist/$', jsonlist.as_view(), name='jsonlist'),
	url(r'^get/$', views.get_stan, name='get_stan'),
	url(r'^stany_mag/$', views.stany_mag, name='stany_mag'),
	url(r'^stany_mag_ue/$', views.stany_mag_ue, name='stany_mag_ue'),
	url(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
]
