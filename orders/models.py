from django.db import models
from django.contrib.auth.models import AbstractUser,User
from products.models import Products
from cart.models import Cart
from userpages.models import Address


# Create your models here.

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name_of_person = models.CharField(max_length=50,blank=True, null=True)
    address = models.ForeignKey(Address,on_delete=models.CASCADE,blank=True, null=True)
    total_amount = models.DecimalField(max_digits=50, decimal_places=2)   
    time_of_order = models.DateTimeField(auto_now_add=True)
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Returned','Returned'),
    )
    status = models.CharField(choices=STATUS,default='Order Confirmed')


class Ordered_Product(models.Model):
    order_id =  models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    product  =  models.ForeignKey(Products,on_delete=models.CASCADE,blank=True, null=True )
    quantity = models.BigIntegerField()
    amount   = models.DecimalField(max_digits=20, decimal_places=2)
    
    
    