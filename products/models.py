from django.db import models
from django.contrib.auth.models import AbstractUser,User



# Create your models here.

class Brand(models.Model):
    name =  models.CharField(default='Shooop', max_length=40)   
    description = models.CharField(max_length=400,blank=True)
    image = models.FileField(upload_to='photos/brands',blank=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
 
class Occassion(models.Model):
        casual = models.CharField(blank=False, max_length=50, default="Casuals")
        Formal = models.CharField(blank=False, max_length=50, default="Formals")
        Sports = models.CharField(blank=False, max_length=50, default="Sports")
    
class Products(models.Model):
    prod_name = models.CharField(blank=False, max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, max_length=40, null=True)
    color = models.CharField(blank=False, max_length=40)
    size = models.IntegerField(blank=False)
    occassion = models.CharField(blank=False, max_length=40)
    ideal_for = models.CharField(blank=False, max_length=40)
    descr = models.CharField(max_length=400,blank=True)
    image = models.FileField(upload_to='photos/products',blank=True)
    offers = models.ForeignKey("products.Offers", on_delete=models.CASCADE, blank=True, null=True)
    coupon = models.ForeignKey("products.Coupons", on_delete=models.CASCADE, blank=True, null=True)
    stock = models.IntegerField(blank=True)
    price = models.IntegerField(blank=False)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.prod_name
    
    
class Variation(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, max_length=40, null=True)
    size = models.IntegerField(null=True, blank=True)    
    stock = models.BigIntegerField(blank=True, default=0)
    price = models.BigIntegerField(blank=False, default=3000)
    discounted_price = models.BigIntegerField(blank=True, null=True)
    
    def offer_price(self):
        offer = self.product.offers
        if offer:
            discount_percentage = offer.discount
            new_price = self.price - (self.price * discount_percentage / 100)
            self.discounted_price = new_price
            self.save()
            return self.discounted_price
    
    
    
class Offers(models.Model):
    name=models.CharField(max_length=50, null=True)
    descr=models.CharField(max_length=550)
    discount=models.IntegerField(blank=False)
    start_date = models.DateField()
    end_date=models.DateField()
    
    def __str__(self):
        return self.name

    
class Coupons(models.Model):
    code = models.CharField(max_length=50, blank=False,unique=True)
    discount = models.IntegerField(blank=False, default=100)
    is_expired = models.BooleanField(default=False)
    minimum_price = models.BigIntegerField(blank=False, default=4000)
       
        
    def __str__(self):
        return self.code  
    
    
    

        
    
    
    

    
    
    
    
  