from django.contrib import admin
from products.models import Products, Offers, Coupons
from userpages.models import Address
from cart.models import Cart
from orders.models import Order, Ordered_Product


# Register your models here.
class Products_Admin(admin.ModelAdmin):
    list_display = ('id','prod_name', 'brand', 'color', 'size', 'occassion', 'ideal_for', 'descr', 'image', 'offers', 'coupon', 'stock', 'price',)
    
       
class Coupons_Admin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_till',)     
   
    
class Offers_Admin(admin.ModelAdmin):
    list_display = ('descr','discount', 'start_date', 'end_date',)  
    
class Address_admin(admin.ModelAdmin):
    list_display = ('id', 'house', 'city', 'state', 'zip', 'country', 'customer')  
    
class Cart_admin(admin.ModelAdmin):
    list_display = ('id', 'customer_id', 'product_id', 'product_count', 'total_price')  
    
class Order_admin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'name_of_person', 'address', 'total_amount', 'time_of_order', 'status') 
    
class Ordered_Product_admin(admin.ModelAdmin) :
    list_display = ('order_id','product','quantity','amount')      
                

admin.site.register(Products, Products_Admin)
admin.site.register(Offers, Offers_Admin)
admin.site.register(Coupons, Coupons_Admin)
admin.site.register(Address, Address_admin)
admin.site.register(Cart, Cart_admin)
admin.site.register(Order, Order_admin)
admin.site.register(Ordered_Product, Ordered_Product_admin)





