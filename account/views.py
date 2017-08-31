from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import ListView
from django.contrib.auth.models import User
from orders.models import Order
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required


class DashboardView(generic.ListView):
    model = User
    paginate_by = 25
    template_name = 'account/dashboard.html'
    context_object_name = 'dashboard'

    @method_decorator(login_required(login_url='/account/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context["orders"] = Order.objects.filter(buyer=self.request.user)
        return context
