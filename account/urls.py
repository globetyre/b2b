from django.conf.urls import url
from . import views
from . views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
	# login / logout urls
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),
	url(r'^logout-then-login/$', auth_views.logout_then_login, {'template_name': 'registration/logout.html'}, name='logout_then_login'),
	url(r'^$', views.DashboardView.as_view(), name='dashboard'),
]
