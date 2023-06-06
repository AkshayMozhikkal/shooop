from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_display, name='products_display'),
    path('single_product/<int:prod_id>', views.single_product, name='single_product'),
  
]