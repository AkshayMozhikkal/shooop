from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login' ),
    path('signup/', views.signup, name='signup' ),
    path('shop/', views.shop, name='shop' ),
    path('product_search/', views.product_search, name='product_search'),
    path('brand_filter/<int:brand_id>', views.brand_filter, name='brand_filter' ),
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
    path('proceedtopay/', views.razorpaycheck, name='proceedtopay'),
    path('cancel_order/<int:ord>', views.cancel_order, name='cancel_order'),
    path('return_item/', views.return_item, name='return_item'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('occassion_filter/<str:occ>/<str:sex>', views.occassion_filter, name='occassion_filter'),
    
    
]