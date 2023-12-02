from django.db import models
from products.models import Products, Variation, Brand, Coupons, Offers
from cart.models import Cart
from userpages.models import Address , User


# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name_of_person = models.CharField(max_length=50,blank=True, null=True)
    phone =models.BigIntegerField(null=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,blank=True, null=True)
    total_amount = models.DecimalField(max_digits=50, decimal_places=2)   
    time_of_order = models.DateTimeField(auto_now_add=True)
    mode_of_payment = models.CharField(max_length=50,blank=True, null=True)
    


class Ordered_Product(models.Model):
    order_id =  models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product  =  models.ForeignKey(Variation,on_delete=models.CASCADE,blank=True, null=True )
    quantity = models.BigIntegerField()
    amount   = models.DecimalField(max_digits=20, decimal_places=2)
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    status = models.CharField(choices=STATUS,default='Order Confirmed', max_length=100)
 
 
 
class Returned(models.Model):
    returned_product =  models.ForeignKey(Ordered_Product, on_delete=models.CASCADE, blank=True, null=True)  
    reason           =   models.CharField(max_length=50, blank=True,null=True)
    comments         =  models.CharField(max_length=250, blank=True,null=True)



class Used_Coupon(models.Model):
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE, blank=True, null=True )
    order  = models.ForeignKey(Order,on_delete=models.CASCADE, blank=True, null=True )       
    new_total_amount = models.BigIntegerField(null=True)
    
    
    