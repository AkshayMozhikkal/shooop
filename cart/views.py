from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from .models import Cart
from products.models import Products, Variation, Brand, Coupons, Offers
from django.contrib import messages, auth
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.



@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def add_to_cart(request,prod_id):
    
    variant = Variation.objects.get(id=prod_id)
    
    if Cart.objects.filter(product_id=variant, customer_id=request.user).exists():
        messages.error(request, 'Item already added before')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     
    users_cart = Cart(customer_id = request.user, product_id = variant, total_price = variant.price)
    if users_cart.product_id.product.offers:
        users_cart.total_price = users_cart.product_id.offer_price()
    users_cart.save()
    
    messages.error(request, 'Item added to cart..!')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    



@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def increase_count(request):
    prod_id = int(request.POST.get('prod_id'))
    price =int(request.POST.get('prod_price'))
       
    cart_item = Cart.objects.get(id= prod_id)
    if cart_item.product_id.product.offers:
        price = int( cart_item.product_id.offer_price())
    
    if cart_item.product_count == cart_item.product_id.stock:
        messages.error(request, 'Maximum quantity reached..!!')
        return JsonResponse({'message': 'Maximum quantity reached..!!',})
    else:
        cart_item.product_count+=1
        cart_item.total_price += price
        cart_item.save()
        return JsonResponse({'message': 'Quantity increased..',})
    
    
 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required   
def decrease_count(request):
    prod_id = int(request.POST.get('prod_id'))
    price =int(request.POST.get('prod_price'))
    
    cart_item = Cart.objects.get(id= prod_id)
    if cart_item.product_id.product.offers:
        price = int( cart_item.product_id.offer_price())
    if cart_item.product_count == 1:
        cart_item.delete()
        return JsonResponse({'message': 'Item removed',})
    else:
        cart_item.total_price -= price
        cart_item.product_count-=1
        cart_item.save()
        return JsonResponse({'message': 'Quantity decreased..',})
        
        
           

@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def cart_remove(request):
    prod_id = int(request.POST.get('prod_id'))
    
    obj = Cart.objects.get(id=prod_id)
    obj.delete()
    messages.error(request, "Item Removed")
    return JsonResponse({'message': 'Item Removed',})
    
    
