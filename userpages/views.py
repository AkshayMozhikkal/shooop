from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from userpages.models import Address
from products.models import Products
from cart.models import Cart, Wishlist
from orders.models import Order, Ordered_Product
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def home(request):
    return render(request,"user/home.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        
        user = auth.authenticate(username =new_username, password=new_password)
        if user is not None:
            auth.login(request, user)
            return redirect('profile') 
        else:
            messages.error(request, 'You dont have an account, Please sign up to get an account..!!')
            return redirect('login') 
    return  render(request, 'user/login.html') 

 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required      
def logout(request):
     auth.logout(request)
     return redirect('login')       
    

def signup(request):
    if request.method == 'POST':
        fname= request.POST['first_name']
        lname= request.POST['last_name']
        username=request.POST['username']
        email= request.POST['email']
        password1= request.POST.get('password1')
        password2= request.POST.get('password2')
        
        if password1 == password2:
            try:
                validate_password(password1)
            except ValidationError as e:
            # Handle the validation error
                error_message = ', '.join(e.messages)
                messages.error(request, error_message)
                return render(request,'user/signup.html')
            
            if User.objects.filter(email=email).exists():
                messages.info(request,'You already registered before, please login with your password..!')
                return redirect('signup')  
            else:
                user = User.objects.create_user(first_name = fname, last_name = lname, username = username, email = email, password = password1) 
                user.save()
                messages.success(request, 'Hi '+user.first_name+', please login now..!!')
                return redirect('login')
        else:
            messages.error(request, 'Password missmatch, enter again')
            return redirect('signup')    
                 
    return render(request,"user/signup.html")



@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def shop(request):
    prod = Products.objects.all().order_by('id')
    products_data = {
        'product': prod
    }
    return render(request,"user/shop.html",products_data)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def profile(request):
    
    user = User.objects.get(username = request.user)
    address = Address.objects.filter(customer = request.user)
    
    context = {
        'user': user,
        'addresses': address
    }
    
    if request.method == 'POST':
        image = request.FILES.get('image')
        username = request.POST.get('username')
        f_name = request.POST.get('first_name')
        l_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
       
        
        user.first_name = f_name
        user.last_name = l_name
        user.username =username
        user.email = email
        user.phone = phone
        if image:
            user.image = image
        
        user.save()
        return redirect('profile')
                
    return render(request,"user/profile.html", context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def add_address(request):
    
    new_house = request.POST.get('house1')
    new_city = request.POST.get('city1')
    new_state = request.POST.get('state1')
    new_zip = request.POST.get('zip1')
    new_country = request.POST.get('country1')
    
    exist= Address.objects.filter(customer=request.user,house=new_house, city=new_city, state=new_state, zip=new_zip, country=new_country)
    if exist:
            messages.error(request, "Address Already exist")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        if new_house:   
                if new_zip:
                    address = Address(customer=request.user, house=new_house, city=new_city, state=new_state, zip=new_zip, country =new_country)
                    address.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    messages.error(request, "Address Must have house number and ZIP/PIN code")             
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
    
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def update_address(request, adrs_id):
    
    address = Address.objects.get(id= adrs_id)
    if request.method == 'POST':
        new_house = request.POST.get('house1')
        new_city = request.POST.get('city1')
        new_state = request.POST.get('state1')
        new_zip = request.POST.get('zip1')
        new_country = request.POST.get('country1')
        
        exist= Address.objects.filter(customer=request.user,house=new_house, city=new_city, state=new_state, zip=new_zip, country=new_country)
        if exist:
            messages.error(request, "Address Already exist")
            return redirect('profile')
        else:
            if new_house:
                address.house = new_house
            if new_city:    
                address.city = new_city
            if new_state:
                address.state = new_state
            if new_zip:
                address.zip = new_zip
            if new_country:
                address.country = new_country
        
            address.save()
            return redirect('profile')



@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required        
def delete_address(request, addr_id):
    address = Address.objects.get(id=addr_id) 
    address.is_active = False
    address.save()
    messages.info(request,"Address deleted successfully..!!")  
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))     
        
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user)
    ordererd_products = Ordered_Product.objects.all() 
    
    context={
      'orders' : orders, 
      'ord_products': ordererd_products
    }
    return render(request,"user/my_orders.html",context)




def add_to_wishlist(request,prod):
    product=Products.objects.get(id=prod)
    exist = Wishlist.objects.filter(customer=request.user, product=product)
    if not exist:
        obj=Wishlist(customer=request.user, product=product)
        obj.save()
        
    return redirect("shop")




def wishlist_remove(request,prod):
    product = Wishlist.objects.get(id=prod)
    product.delete()
    return redirect('wishlist')



def wishlist(request):
    
    wishlist = Wishlist.objects.filter(customer=request.user)
        
    context={
        'wishlist': wishlist
    }
    return render(request,"user/wishlist.html",context)




def cart(request):
    total_price = 0
    cart_object = Cart.objects.filter(customer_id = request.user).order_by('id')
    for i in cart_object:
        total_price = total_price + i.total_price
    
        
   
    context = {
        'cart_obj' : cart_object,
        'total_price' : total_price,
    }
             
    
    return render(request,"user/cart.html", context)



    
  
def checkout(request):
    user = request.user
    address = Address.objects.filter(customer=request.user)
    cart= Cart.objects.filter(customer_id= request.user)
    
    total_price = 0
    for i in cart:
        total_price = total_price + i.total_price
    
    context ={
        'user': user,
        'address': address,
        'cart': cart,
        'total_price':total_price
    }
    
    return render(request,"user/checkout.html",context )


@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def place_order(request):
    user= request.user
    if request.method == 'POST':
        name = request.POST.get('first_name')
        mode_of_payment = request.POST.get('selector')
        selected_address = request.POST.get('delivery_address')
        
        if mode_of_payment != 'COD':
            messages.info(request,'Please select Cash On Delivery..!')
            return redirect('checkout')
        if selected_address:
            address = Address.objects.get(id=selected_address)
        else:    
            messages.error(request,'Please select an address..!!')
            return redirect('checkout')
            
        ordered_products = Cart.objects.filter(customer_id = user)
        
        if ordered_products:
            amount = 0
            for i in ordered_products:
                amount = amount + i.total_price
                i.product_id.stock = i.product_id.stock - i.product_count
                i.product_id.save()
                
            order = Order(customer = user, name_of_person= name, address=address, total_amount=amount)
            order.save()
            
            for item in ordered_products:
                object=Ordered_Product(order_id=order, product=item.product_id, quantity=item.product_count, amount=item.total_price)
                object.save()
            
            return render(request,'user/order_confirmed.html',{"order":order, "products": ordered_products})
        
        else:
            messages.error(request,'Cannot place an order. Your Cart is empty..!!')
            return redirect('checkout')
        
    return redirect('checkout')    
    
    

        

