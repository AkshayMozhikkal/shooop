from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .models import Products, Variation

# Create your views here.

@login_required
def products_display(request):
    return render(request, 'admins/products.html')



def single_product(request,prod_id, var):
    
    if var ==0:
        prod = Products.objects.get(id =prod_id)
        variations = Variation.objects.filter(product__id=prod_id)
        return render(request, 'user/single_product.html',{"product":prod, "variations": variations})
    else:
        variant = Variation.objects.get(id=var)
        variations = Variation.objects.filter(product__id=variant.product.id)
        return render(request, 'user/single_product.html',{"product":variant, "variations": variations, "second":True})