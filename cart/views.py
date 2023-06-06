from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from .models import Cart
from products.models import Products
from django.contrib import messages, auth
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


# Create your views here.



def add_to_cart(request,prod_id):
    
    product = Products.objects.get(id=prod_id)
    
    if Cart.objects.filter(product_id=product, customer_id=request.user).exists():
        messages.error(request, 'Item Already added before')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
     
    users_cart = Cart(customer_id = request.user, product_id = product, total_price = product.price)
    users_cart.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    



def increase_count(request):
    prod_id = int(request.POST.get('prod_id'))
    price =int(request.POST.get('prod_price'))
    
    cart_item = Cart.objects.get(id= prod_id)
    if cart_item.product_count == cart_item.product_id.stock:
        messages.error(request, 'Maximum quantity reached..!!')
        return redirect('cart')
    else:
        cart_item.product_count+=1
        cart_item.total_price += price
        cart_item.save()
        return JsonResponse({'message': 'Form submitted successfully',})
    
    
    
def decrease_count(request):
    prod_id = int(request.POST.get('prod_id'))
    price =int(request.POST.get('prod_price'))
    
    cart_item = Cart.objects.get(id= prod_id)
    if cart_item.product_count == 1:
        cart_item.delete()
        return redirect('cart')
    else:
        cart_item.total_price -= price
        cart_item.product_count-=1
        cart_item.save()
        return redirect('cart')
        
        
           

def cart_remove(request):
    prod_id = int(request.POST.get('prod_id'))
    
    obj = Cart.objects.get(id=prod_id)
    obj.delete()
    messages.success(request, "Item Removed")
    return redirect('cart')
    
