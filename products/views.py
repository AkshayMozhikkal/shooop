from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Products

# Create your views here.

@login_required
def products_display(request):
    return render(request, 'admins/products.html')


@login_required
def single_product(request,prod_id):
    prod = Products.objects.get(id =prod_id)
    return render(request, 'user/single_product.html',{"product":prod})