from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    wallet = models.BigIntegerField(blank=True, default=0, null=True)   
    phone = models.BigIntegerField(blank=True, default=0, null=True)   
    
class Address(models.Model):
    house = models.CharField(blank=True,null=True, max_length=50)
    city = models.CharField(blank=True,null=True, max_length=50)
    state = models.CharField(blank=True,null=True, max_length=50)
    zip = models.CharField(blank=True,null=True, max_length=50)
    country = models.CharField(blank=True,null=True, max_length=50)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    

class User_otp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    otp = models.BigIntegerField()



    

    