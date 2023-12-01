from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect, JsonResponse
from django.contrib import messages, auth
from django.contrib.auth import authenticate 
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from userpages.models import Address, User_otp
from products.models import Products , Variation, Offers, Coupons, Brand,Occassion
from cart.models import Cart, Wishlist
from orders.models import Order, Ordered_Product, Returned, Used_Coupon
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import random
import re
from razorpay import Client
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q




def home(request):
    context ={
        'products': Products.objects.all().order_by('id'),
        'brands' : Brand.objects.all()
    }
    return render(request,"user/home.html", context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=new_username)
            if not user.is_active:
                 messages.error(request, 'Account is blocked, please enquire for more details..!!')
                 return redirect('login') 
                
        except:
            user = None
        
        user = auth.authenticate(username =new_username.strip(), password=new_password)
           
        if user is not None:
            auth.login(request, user)
            return redirect('profile') 
        else:
            messages.error(request, 'Please check the Username and Password you entered..!!')
            return redirect('login') 
    return  render(request, 'user/login.html') 



# Forgot Password
def forgot_password(request):
    if request.method=='POST':
        new_password = request.POST.get('new_pass1')
        n_password = request.POST.get('new_pass2')
        if new_password:
            user_email =request.POST.get('email')
            userrr = User.objects.get(email=user_email)
            User_otp.objects.filter(user=userrr).delete()
            
            
            if new_password != n_password:
                messages.success(request,"Password Missmatch, Enter again..")
                return render(request,'forgot_password.html',{'otp':False,'usr':userrr, 'reset': True})
            else:
                try:
                    validate_password(new_password)
                except ValidationError as e:
                # Handle the validation error
                    error_message = ', '.join(e.messages)
                    messages.error(request, error_message)
                    return render(request,'forgot_password.html',{'otp':False,'usr':userrr, 'reset': True})
                
                userrr.set_password(new_password)
                userrr.save()
                messages.success(request,"Password Updated Successfully, please login now..!")
                return redirect('login')
            
            
        get_otp = request.POST.get('otp')
        if get_otp:
           get_email =request.POST.get('email')
           userr = User.objects.get(email=get_email)
           
           
           if int(get_otp) == User_otp.objects.filter(user=userr).last().otp:
               
               messages.success(request,"OTP Verified..! Now reset your Password")
               return render(request,'forgot_password.html',{'otp':False,'usr':userr, 'reset': True})
           else:
               messages.success(request,"You entered a wrong OTP, please try again..!!")
               return render(request,'forgot_password.html',{'otp':True,'usr':userr})
           
           
        else:   
            email = request.POST.get('email')
            if email:
                email.strip()
                try:
                    uuser = User.objects.get(email=email)
                except:
                    uuser = None    
                if uuser:
                    user_otp=random.randint(100000,999999)
                    User_otp.objects.create(user=uuser, otp=user_otp)
                    mess=f'Hello\t{uuser.first_name},\nOTP to verify your account for SHOOOP is {user_otp}\nThank You..!!'
                    send_mail(
                            "Welcome to SHOOOP, Verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [uuser.email],
                            fail_silently=False
                        )
                    return render(request,'forgot_password.html',{'otp':True,'usr':uuser})
                else:
                    messages.success(request,"You are not registered yet, please signup..!!")    
                    return render(request,'forgot_password.html')
            
                    
                    
            else:
                messages.success(request,"Please enter your Email ID to send OTP")    
                return render(request,'forgot_password.html')
        
        
    return render(request,'forgot_password.html')


# Reset Password 

@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def reset_password(request):
   curr_pass = request.POST.get('curr_pass')
   new_pass1 = request.POST.get('new_pass')
   new_pass2 = request.POST.get('new_pass2')
   
   user = request.user
  
   if check_password(curr_pass,user.password ):
       if new_pass1 == new_pass2:
            try:
                validate_password(new_pass1)
            except ValidationError as e:
                # Handle the validation error
                error_message = ', '.join(e.messages)
                messages.error(request, error_message)
                return render(request,'user/profile.html')
            user.set_password(new_pass1)
            user.save()
            messages.success(request,"Password Updated Successfully, Login Now..!")    
            return redirect('login')
       else:
            messages.success(request,"Passwords Missmatch..")    
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
           
   else:
        messages.success(request,"Please enter your correct password")    
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

    
    
    
    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required      
def logout(request):
     auth.logout(request)
     return redirect('login')       

def validateEmail(email):
    from django.core.validators import validate_email
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
    

def signup(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp:
            get_email=request.POST.get('email')
            usr=User.objects.get(email=get_email)
            if int(otp)==User_otp.objects.filter(user=usr).last().otp:
                usr.is_active=True
                usr.save()
                auth.login(request,usr)
                messages.success(request,f'Account is created for {usr.email}')
                User_otp.objects.filter(user=usr).delete()
                return redirect('profile')
            else:
                messages.warning(request,f'You Entered a wrong OTP')
                return render(request,'user/signup.html',{'otp':True,'usr':usr})

        else:    
            fname= request.POST['first_name']
            lname= request.POST['last_name']
            username=request.POST['username']
            email= request.POST['email']
            password1= request.POST.get('password1')
            password2= request.POST.get('password2')
            
            result = validateEmail(email)
            if result is False:  
                messages.info(request,'Please enter a valid Email ID')
                return redirect('signup') 
            

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
                    user = User.objects.create_user(first_name = fname, last_name = lname, username = username, email = email, password = password1, phone=0)
                    user.is_active = False 
                    user.save()
                    
                    user_otp=random.randint(100000,999999)
                    User_otp.objects.create(user=user, otp=user_otp)
                    mess=f'Hello\t{user.first_name},\nOTP to verify your account for SHOOOP is {user_otp}\nHappy Shopping..!!'
                    send_mail(
                            "Welcome to SHOOOP, Verify your Email",
                            mess,
                            settings.EMAIL_HOST_USER,
                            [user.email],
                            fail_silently=False
                        )
                    return render(request,'user/signup.html',{'otp':True,'usr':user})
                
            else:
                messages.error(request, 'Password missmatch, enter again')
                return redirect('signup')    
                 
    return render(request,"user/signup.html")


#Shop Page
def shop(request):
    
    products_data = {
            'occassion': Occassion.objects.all(),
            'product':Products.objects.all().order_by('id'),
            'brands' : Brand.objects.all()
        }
                    
    return render(request,"user/shop.html",products_data)

# Occassion Filter
def occassion_filter(request,occ,sex):
    products_data = {
            'occassion': Occassion.objects.all(),
            'product':Products.objects.filter(occassion=occ, ideal_for=sex).order_by('id'),
            'brands' : Brand.objects.all()
        }
    messages.error(request, occ+' for '+sex)
    return render(request,"user/shop.html",products_data)

# Product Search
def product_search(request):
    key = request.GET.get('key')
    
    products_data = {
            'occassion': Occassion.objects.all(),
            'product':Products.objects.filter(Q(brand__name__icontains=key) |Q(prod_name__icontains=key) | Q(color__icontains=key) | Q(descr__icontains=key) | Q(occassion__icontains=key) | Q(ideal_for__icontains=key)),
            'brands' : Brand.objects.all()
        }
    
    messages.error(request,"Products matching : "+key)
    return render(request,"user/shop.html",products_data)




def brand_filter(request, brand_id):
    brnd_name = Brand.objects.get(id=brand_id).name
    products_data = {
            'occassion': Occassion.objects.all(),
            'product':Products.objects.filter(brand__id=brand_id),
            'brands' : Brand.objects.all()
        }
    messages.error(request, brnd_name+" shoes in shop")
    return render(request,"user/shop.html",products_data)



# Profile Page
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
        # email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        # Validations
        if f_name == '' and username == '' and email == '':
            messages.error(request, "Fields can't be blank")
            return redirect('profile')
        try:
            usr =  User.objects.get(username=username)
        except User.DoesNotExist:
            usr = None
        if usr:
            if usr.username != user.username:
                messages.info(request,'Username already taken, please try another')
                return redirect('profile') 
        # result = validateEmail(email)
        # if result is False:  
        #     messages.info(request,'Please enter a valid Email ID')
        #     return redirect('profile') 
        # if f_name.strip() == '' or username.strip() == '':
        #     messages.error(request, "Fields can't be blank")
        #     return redirect('profile')
        
        # Data Assigning
        if f_name:
            user.first_name = f_name.strip()
        user.last_name = l_name
        if username:
            user.username =username.strip()
        # if email:
        #     user.email = email.strip()
        if phone:
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
    try:
        exist= Address.objects.filter(customer=request.user,house=new_house, city=new_city, state=new_state, zip=new_zip, country=new_country)
    except Address.DoesNotExist:
        exist = None
    
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
    orders = Order.objects.filter(customer=request.user).order_by('-id')
    ordererd_products = Ordered_Product.objects.all().order_by('id') 
    coupons_used= Used_Coupon.objects.filter(order__customer=request.user)
   
    
    context={
      'orders' : orders, 
      'ord_products': ordererd_products,
      'coupons_used':coupons_used
    }
    return render(request,"user/my_orders.html",context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def add_to_wishlist(request,prod):
    product=Products.objects.get(id=prod)
    exist = Wishlist.objects.filter(customer=request.user, product=product)
    if not exist:
        obj=Wishlist(customer=request.user, product=product)
        obj.save()
        messages.success(request, 'Item added to Wishlist..!!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'Item Already added before')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
    



@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def wishlist_remove(request,prod):
    product = Wishlist.objects.get(id=prod)
    product.delete()
    return redirect('wishlist')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def wishlist(request):
    
    wishlist = Wishlist.objects.filter(customer=request.user)
        
    context={
        'wishlist': wishlist
    }
    return render(request,"user/wishlist.html",context)



@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
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



    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required  
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
        order_total = request.POST.get('order_total')
        new_price = request.POST.get('new_price')
        coupon_code2 = request.POST.get('coupon_code2')
        name = request.POST.get('first_name')
        phone = request.POST.get('phone')
        mode_of_payment = request.POST.get('selector')
        selected_address = request.POST.get('delivery_address')
        
        
        
        if mode_of_payment != 'Razorpay':
            if not phone or phone == '0':
                messages.error(request,'Please add a contact number..!!')
                return redirect('checkout') 
        if not mode_of_payment:
            messages.error(request,'Please select a payment method..!!')
            return redirect('checkout')            
        if mode_of_payment != 'COD':
            if mode_of_payment != 'Razorpay':
                messages.error(request,'Please select Cash On Delivery or RazorPay..!!')
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
                
            if new_price:
                    amount = new_price
                    
                    
            order = Order(customer = user, name_of_person= name, phone=phone, address=address, mode_of_payment=mode_of_payment, total_amount=amount)
            order.save()
            
            if new_price:
                Used_Coupon.objects.create(coupon = Coupons.objects.filter(code=coupon_code2).first(), order = order, new_total_amount=new_price)
            
            for item in ordered_products:
                object=Ordered_Product(order_id=order, product=item.product_id, quantity=item.product_count, amount=item.total_price)
                object.save()
                item.delete()
                
            if mode_of_payment == "Razorpay":
                return JsonResponse({'status' : "Your order has been placed successfully"})
            
            messages.info(request,'Order Placed')
            return render(request,'user/order_confirmed.html',{"order":order, "products": Ordered_Product.objects.filter(order_id=order.id)})

        
        else:
            messages.error(request,'Cannot place an order. Your Cart is empty..!!')
            return redirect('checkout')
        
    return redirect('checkout')  


# Apply Coupon
def apply_coupon(request):
    coupon_code = request.POST.get('coupon_code')
    order_total = request.POST.get('order_total')
    order_total = float(order_total)
    # To Avoid spaces
    coupon_code = coupon_code.strip()
    
    coupon = Coupons.objects.filter(code=coupon_code).first()
    
    if coupon:
        if not coupon.is_expired:
            coupon_used = Used_Coupon.objects.filter(coupon__id=coupon.id, order__customer=request.user)
            if coupon_used:
                return JsonResponse({'status': 'You already used this Coupon..!!'})
            else:
                if order_total > coupon.minimum_price:
                    new_total = order_total - coupon.discount
                    return JsonResponse({'status': 'Coupon Applied..!!','new_total':new_total,'coupon_discount':coupon.discount, 'coupon_code':coupon_code})
                else:
                    return JsonResponse({'status': 'Order Amount Not Eligible for this Coupon..!!',})    
        else:
            return JsonResponse({'status': 'Coupon Expired',})    
        
    else:    
        return JsonResponse({'status': 'Not a Valid Coupon..!!'})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def cancel_order(request,ord):
   customer = request.user
   ord_prod = Ordered_Product.objects.get(id=ord)
   
   
   ord_prod.status = 'Cancelled' 
   if ord_prod.order_id.mode_of_payment != "COD":
        customer.wallet = customer.wallet + ord_prod.amount
   ord_prod.product.stock += ord_prod.quantity
   ord_prod.order_id.total_amount -= ord_prod.amount
   ord_prod.order_id.save()
   ord_prod.product.save()
   ord_prod.save()
   customer.save()


   messages.error(request,'Order Cancelled..!!')
   if ord_prod.order_id.mode_of_payment != "COD":
        messages.error(request,'Amount Refunded to your Wallet..!!')
   return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def return_item(request):
    if request.method == 'POST':
        ord_id = request.POST.get('item')
        reason = request.POST.get('return_reason')
        note = request.POST.get('return_comment')
        
        return_product = Ordered_Product.objects.get(id=ord_id)
        Returned.objects.create(returned_product = return_product, reason = reason, comments = note)
        
        return_product.status = 'Returned'
    
        request.user.wallet += return_product.amount
        
        return_product.save()
        request.user.save()
        
        if reason == 'Ordered by mistake' or reason == 'Wrong item':
            return_product.product.stock += return_product.quantity
            return_product.product.save()
        
        
        messages.error(request,'Item return initiated, will be processed in 2 days, please see the amount in your Wallet..')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))     
            
            


@cache_control(no_cache=True, must_revalidate=True, no_store=True)     
@login_required
def razorpaycheck(request):
    new_price = request.GET.get('new_price')
    coupon_code2 = request.GET.get('coupon_code2')
    
    
    ordered_products = Cart.objects.filter(customer_id = request.user)
        
    if ordered_products:
        total_price = 0
        for i in ordered_products:
            total_price = total_price + i.total_price
    if  new_price:
        total_price = new_price       
    return  JsonResponse({
        
        'total_price':total_price,
        'coupon_code2':coupon_code2,
    })       

  

        









    