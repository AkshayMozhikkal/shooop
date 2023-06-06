from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:prod_id>', views.add_to_cart, name='add_to_cart'),
    path('cart_remove/', views.cart_remove, name='cart_remove'),
    path('increase_count/', views.increase_count, name='increase_count'),
    path('decrease_count/', views.decrease_count, name='decrease_count'),
    
]