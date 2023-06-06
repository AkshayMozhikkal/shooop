from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from products.models import Products
from userpages.models import Address
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from products.models import Products
from orders.models import Order, Ordered_Product
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_login')
def dashboard(request):
    if request.user.is_superuser:
        return render(request, 'admins/dashboard.html')
    else:
        return render (request, 'user/home.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.method =='POST':
        new_username = request.POST['username']
        new_password = request.POST['password']
        
        user = authenticate(username=new_username, password = new_password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('dashboard')
        else:
            return redirect('admin_login')
        
    return render(request, 'admins/dashboard_login.html')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def products(request):
    prod= Products.objects.all().order_by('id')
    products_data = {
    "product": prod
}
    return render(request, 'admins/products.html',products_data)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_product(request):
    
    if request.method == 'POST':
        prod_name = request.POST.get('prod_name')
        brand = request.POST.get('brand')
        color = request.POST.get('color')
        size = request.POST.get('size')
        occassion = request.POST.get('occassion')
        ideal_for = request.POST.get('ideal_for')
        descr = request.POST.get('descr')
        image = request.FILES.get('image')
        offers = request.POST.get('offers')
        coupon = request.POST.get('coupon')
        stock = request.POST.get('stock')   
        price = request.POST.get('price')
        
        new_product = Products(prod_name=prod_name,brand=brand,color=color,size=size, occassion=occassion,ideal_for=ideal_for,descr=descr, image=image,stock=stock,price=price)
        new_product.save()
        return redirect('products')
    return render(request,'admins/add_product.html')


@login_required 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def update_product(request, prod_id):
    if request.method == 'POST':
        prod_name = request.POST.get('prod_name')
        brand = request.POST.get('brand')
        color = request.POST.get('color')
        size = request.POST.get('size')
        occassion = request.POST.get('occassion')
        ideal_for = request.POST.get('ideal_for')
        descr = request.POST.get('descr')
        image = request.FILES.get('image')
        offers = request.POST.get('offers')
        coupon = request.POST.get('coupon')
        stock = request.POST.get('stock')   
        price = request.POST.get('price')
        
        product = Products.objects.get(id = prod_id)
        
        product.prod_name = prod_name
        product.brand = brand
        product.prod_name = prod_name
        product.color = color
        product.size = size
        product.occassion = occassion
        product.ideal_for = ideal_for
        product.descr = descr
        if image:
            product.image = image
        product.stock = stock
        product.price = price
        
        product.save()
        messages.success(request, 'Updated successfully')
        return redirect('products')
        
        
    prod = Products.objects.get(id = prod_id)
    return render(request, 'admins/update_product.html', { 'item':prod }) 


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_product(request, prod_id):
    prod = Products.objects.get(id = prod_id)
    prod.delete()
    return redirect('products')

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def users_list(request):
    
    user = User.objects.all().order_by('id')
    address = Address.objects.all()
    user_dict = {
        "persons": user ,
        "addresses" : address   
    }
    return render(request, 'admins/users_list.html',user_dict)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required   
def send_unblock_email(user_email, username):
    subject = 'Account Unblocked'
    html_message = render_to_string('unblock_email.html', {'username': username})
    plain_message = strip_tags(html_message)
    from_email = 'emailcollector.django@gmail.com'  # Replace with your email address or a custom sender
    recipient_list = [user_email]

    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)   
    
    

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_user(request, user_id):
    user = User.objects.get(id = user_id)
    if user.is_active:
        user.is_active = False
        user.save()
        return redirect('users_list')
    
    else : 
        user.is_active = True
        user.save()
        send_unblock_email(user.email, user.username)
        return redirect('users_list')
    
    
 
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def orders_list(request):
    
    context={
        'orders': Order.objects.all().order_by('id'),
        'items' : Ordered_Product.objects.all()
    }
    
    return render(request, 'admins/orders_list.html', context) 



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_order_status(request, order_id):
    order = Order.objects.get(id= order_id)
    order.status = request.POST.get('status')
    order.save()
    return redirect('orders_list')
    
       
    
    
    
    
    
    
    
    