from django.contrib import admin
from products.models import Products, Offers, Coupons, Brand, Variation, Occassion
from userpages.models import Address
from cart.models import Cart
from orders.models import Order, Ordered_Product, Returned, Used_Coupon


# Register your models here.
class Products_Admin(admin.ModelAdmin):
    list_display = ('id','prod_name', 'brand', 'color', 'size', 'occassion', 'ideal_for', 'descr', 'image', 'offers', 'coupon', 'stock', 'price',)
    
       
class Coupons_Admin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'is_expired','minimum_price')     
   
    
class Offers_Admin(admin.ModelAdmin):
    list_display = ('descr','discount', 'start_date', 'end_date',)  
    
class Address_admin(admin.ModelAdmin):
    list_display = ('id', 'house', 'city', 'state', 'zip', 'country', 'customer')  
    
class Cart_admin(admin.ModelAdmin):
    list_display = ('id', 'customer_id', 'product_id', 'product_count', 'total_price')  
    
class Order_admin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'name_of_person', 'address', 'total_amount', 'time_of_order' ) 
    
class Ordered_Product_admin(admin.ModelAdmin) :
    list_display = ('id','order_id','product','quantity','amount','status')     
    
class Variations_Admin(admin.ModelAdmin):
    list_display = ('id','product', 'size', 'stock', 'price', 'discounted_price') 
    
class Brand_Admin(admin.ModelAdmin):
    list_display = ('id','name', 'description', 'image','added_on')           
                

admin.site.register(Products, Products_Admin)
admin.site.register(Offers, Offers_Admin)
admin.site.register(Coupons, Coupons_Admin)
admin.site.register(Address, Address_admin)
admin.site.register(Cart, Cart_admin)
admin.site.register(Order, Order_admin)
admin.site.register(Ordered_Product, Ordered_Product_admin)
admin.site.register(Variation,Variations_Admin)
admin.site.register(Brand,Brand_Admin)
admin.site.register(Returned)
admin.site.register(Occassion)
admin.site.register(Used_Coupon)





