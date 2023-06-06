from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login' ),
    path('signup/', views.signup, name='signup' ),
    path('shop/', views.shop, name='shop' ),
    path('profile/', views.profile, name='profile' ),
    path('update_address/<int:adrs_id>', views.update_address, name='update_address' ),
    path('add_address/', views.add_address, name='add_address' ),
    path('delete_address/<int:addr_id>', views.delete_address, name='delete_address' ),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('add_to_wishlist/<int:prod>', views.add_to_wishlist, name='add_to_wishlist' ),
    path('wishlist_remove/<int:prod>', views.wishlist_remove, name='wishlist_remove' ),
    path('wishlist/', views.wishlist, name='wishlist' ),
    path('checkout/', views.checkout, name='checkout' ),
    path('place_order/', views.place_order, name='place_order' ),
    path('logout/', views.logout, name='logout' ),
    path('cart/', views.cart, name='cart' ),
    
    
    # path('confirmation/', views.confirmation, name='confirmation' ),
]