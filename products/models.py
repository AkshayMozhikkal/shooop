from django.db import models

# Create your models here.
class Products(models.Model):
    prod_name = models.CharField(blank=False, max_length=50)
    brand = models.CharField(blank=False, max_length=40)
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
    
class Offers(models.Model):
    descr=models.CharField(max_length=50)
    discount=models.IntegerField(blank=False)
    start_date = models.DateField()
    end_date=models.DateField()
    
class Coupons(models.Model):
    code=models.IntegerField(blank=False,unique=True)
    discount=models.IntegerField(blank=False)
    valid_till=models.IntegerField()    
        
    
    
    
    
    
  