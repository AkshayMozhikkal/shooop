from django.db import models
from products.models import Products, Variation, Offers, Coupons
from userpages.models import User

# Create your models here.

    
    

class Cart(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Variation, on_delete=models.CASCADE)
    product_count = models.BigIntegerField(default=1)
    total_price = models.BigIntegerField()
    
    
class Wishlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
      