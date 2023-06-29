from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from products.models import Products, Variation, Brand, Offers, Coupons
from userpages.models import Address
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from products.models import Products
from orders.models import Order, Ordered_Product
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.db.models import Sum
from django.db.models.functions import TruncDay
from openpyxl import Workbook
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.views import View
import json



# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='admin_login')
def dashboard(request):
    if request.user.is_superuser:
        sales_by_day = Order.objects.annotate(day=TruncDay('time_of_order')).values('day').annotate(total_sales=Sum('total_amount')).order_by('day')
        print(sales_by_day)
        # Convert sales_by_day queryset to a list of dictionaries
        sales_data = list(sales_by_day.values('day', 'total_sales'))

        # Serialize the data to JSON
        sales_data_json = json.dumps(sales_data, default=str)
        
        context={
            'sales_by_day':sales_by_day,
            'sales_by_day_json':sales_data_json
        }
        return render(request, 'admins/dashboard.html',context)
    else:
        return render (request, 'admins/dashboard_login.html')


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
    context={
        'variations': Variation.objects.all(),
        'brands' : Brand.objects.all().order_by('id'),
        'offers': Offers.objects.all().order_by('id')
    }
    
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
        
        if not price:
            messages.success(request, "Please add price")
            return render(request,'admins/add_product.html', context)
        if not stock:
            messages.success(request, "Please add stock quantity")
            return render(request,'admins/add_product.html', context)
        
        prod_brand = Brand.objects.get(id=brand)
        if offers:
            offer = Offers.objects.get(id=offers)
        try:
            new_product = Products.objects.get(prod_name=prod_name)
        except:
            new_product = Products(prod_name=prod_name, brand=prod_brand, color=color, size=size, occassion=occassion,ideal_for=ideal_for,descr=descr, image=image, offers=offer, stock=stock,price=price)
            new_product.save()  
  
        Variation.objects.create(product=new_product, size= size, price= price, stock = stock)
        return redirect('products')
    
    
    return render(request,'admins/add_product.html', context)


@login_required 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)   
def update_product(request, prod_id):
    
    context={
        'variations': Variation.objects.all(),
        'brands' : Brand.objects.all().order_by('id'),
        'item':Products.objects.get(id = prod_id),
        'offers': Offers.objects.all().order_by('id'),
        'product': Products.objects.get(id=prod_id)
    }
    
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
        
        if prod_name:
            product.prod_name = prod_name
        if brand:    
            product.brand = Brand.objects.get(id=brand)
        if color:
            product.color = color
        if size:
            product.size = size
        if occassion:
            product.occassion = occassion
        if ideal_for:
            product.ideal_for = ideal_for
        if descr:    
            product.descr = descr
        if image:
            product.image = image
        if offers:
            product.offers = Offers.objects.get(id=offers)
        else:
            product.offers = None
                    
        if stock:   
            product.stock = stock
        if price:   
            product.price = price
        
        product.save()
        variant = Variation.objects.filter(product__prod_name = product.prod_name, size= size).first()
        if variant:
            variant.stock = stock
            variant.price = price
            variant.save()
            messages.success(request, 'Updated successfully')
            return redirect('products')
            
        else:
            Variation.objects.create(product = product, size=size, price=price, stock = stock)
            messages.success(request, 'New update added successfully')
            return redirect('products')
            
                
    return render(request, 'admins/update_product.html', context) 


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_product(request, prod_id):
    prod = Products.objects.get(id = prod_id)
    prod.delete()
    return redirect('products')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def users_list(request):
    
    user = User.objects.all().order_by('id')
    address = Address.objects.all()
    user_dict = {
        "persons": user ,
        "addresses" : address   
    }
    return render(request, 'admins/users_list.html',user_dict)



def send_unblock_email(user_email, username):
    subject = 'Account Unblocked'
    html_message = render_to_string('unblock_email.html', {'username': username})
    plain_message = strip_tags(html_message)
    from_email = 'emailcollector.django@gmail.com'  # Replace with your email address or a custom sender
    recipient_list = [user_email]
    send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)   
    
    

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
        'orders': Order.objects.all(),
        'ordered_products' : Ordered_Product.objects.all().order_by('id')
    }
    
    return render(request, 'admins/orders_list.html', context) 



@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_order_status(request, order_id):
    ordered_product = Ordered_Product.objects.get(id= order_id)
    ordered_product.status = request.POST.get('status')
    ordered_product.save()
    return redirect('orders_list')


    
@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def coupons(request):
    if request.method == 'POST':
        coupon_id = request.POST.get('coupon_id')
        code = request.POST.get('code')
        discount = request.POST.get('discount')
        minimum_price = request.POST.get('minimum_price')
        is_expired = request.POST.get('is_expired')
        
        coupon = Coupons.objects.get(id=coupon_id)
        
        # Update Coupon
        coupon.code = code
        coupon.discount = discount
        coupon.minimum_price = minimum_price
        if is_expired:
            coupon.is_expired = is_expired
        
        coupon.save()
        
    
    coupons = Coupons.objects.all().order_by('id')
    return render (request, 'admins/coupons.html',{'coupons':coupons})



def offers_list(request):
    if request.method == 'POST':
        offr_id = request.POST.get('offer_id')
        offr_name=  request.POST.get('name')
        discount=  request.POST.get('discount')
        description=  request.POST.get('description')
        start_date=  request.POST.get('start_date')
        end_date=  request.POST.get('end_date')
        
        offer = Offers.objects.get(id=offr_id)
       
        if offr_name:
            offer.name =offr_name
        if discount:
            offer.discount =discount
        if description:
            offer.descr =description
        if start_date:
            offer.start_date =start_date   
        if end_date:
            offer.end_date =end_date
            
        offer.save() 
        
        messages.success(request, 'New update added successfully')            
        return render(request, 'admins/offers_list.html', {'offers': Offers.objects.all().order_by('id')})
        
        
    return render(request, 'admins/offers_list.html', {'offers': Offers.objects.all().order_by('id')})
    

def add_offer(request):
        offr_name=  request.POST.get('name')
        discount=  request.POST.get('discount')
        description=  request.POST.get('description')
        start_date=  request.POST.get('start_date')
        end_date=  request.POST.get('end_date')
        
        if not start_date:
            messages.success(request, 'Date Field cant be empty..!')
            return redirect('offers_list')
        if not end_date:
            messages.success(request, 'Date Field cant be empty..!')
            return redirect('offers_list')
            
        if offr_name:
            offr_name= offr_name.strip()
            exist = Offers.objects.filter(name= offr_name)
            if exist:
                messages.success(request, 'Offer name already exist..!')
                return redirect('offers_list')
            if discount: 
                Offers.objects.create(name=offr_name, discount= discount, descr= description, start_date= start_date, end_date= end_date)
                return redirect('offers_list') 
            else:
                messages.success(request, 'Please Specify a discount..!')
                return redirect('offers_list')  
                    
        else:
            messages.success(request, 'Offer should have a name..!')
            return redirect('offers_list')  
         
                
            

def add_coupon(request):
    
        code = request.POST.get('code')
        discount = request.POST.get('discount')
        minimum_price = request.POST.get('minimum_price')
        is_expired = request.POST.get('is_expired')
        
        coupon = Coupons.objects.filter(code = code)
        
        if coupon:
            messages.error(request, " Copuon Already exists, please try to edit for changes..")
            return redirect('coupons')
        else:
            Coupons.objects.create(code=code, discount=discount, minimum_price=minimum_price, is_expired=is_expired)
            messages.error(request, " Coupon Created..!!")
            return redirect('coupons')
            
    
def report(request):
    
    context = {}
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        if start_date == '' or end_date == '':
            messages.error(request, 'Give date first')
            return redirect('report')
            
        if start_date == end_date:
            date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            order_items = Order.objects.filter(total_amount__gt=0,time_of_order=date_obj.date())
            if order_items:
                context.update(sales=order_items, s_date=start_date, e_date=end_date)
                return render(request, 'admins/sales_report.html', context)
            else:
                messages.error(request, 'No data found')
            return redirect('report')

        order_items = Order.objects.filter(total_amount__gt=0,time_of_order__gte=start_date, time_of_order__lte=end_date)
        total_revenue = order_items.aggregate(total_revenue=Sum('total_amount'))['total_revenue']
        
        if order_items:
            context.update(sales=order_items, s_date=start_date, e_date=end_date, total_revenue=total_revenue)
        else:
            messages.error(request, 'No data found')
    return render(request, 'admins/sales_report.html',context)


class SalesReportPDFView(View):
    def get(self, request, *args, **kwargs):
        # Generate the PDF content
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 100, "Sales Report")
        # Add more content to the PDF as needed

        # Finish the PDF
        p.showPage()
        p.save()

        # Set the response headers for file download
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
        return response
        
class SalesReportExcelView(View):
    def get(self, request, *args, **kwargs):
        # Generate the Excel content
        wb = Workbook()
        ws = wb.active
        ws['A1'] = "Sales Report"
        # Add more content to the Excel file as needed

        # Save the Excel file
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="sales_report.xlsx"'
        wb.save(response)
        return response
         
    
    
    
    
    
    
    
    