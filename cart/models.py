from django.db import models
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.

    
    

class Cart(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_count = models.BigIntegerField(default=1)
    total_price = models.DecimalField(max_digits=20, decimal_places=2)
    
    
class Wishlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
      