from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('products/',views.products, name='products'),
    path('add_product/',views.add_product, name='add_product'),
    path('update_product/<int:prod_id>',views.update_product, name='update_product'),
    path('delete_product/<int:prod_id>',views.delete_product, name='delete_product'),
    path('users_list/',views.users_list, name='users_list'),
    path('orders_list/',views.orders_list, name='orders_list'),
    path('update_order_status/<int:order_id>',views.update_order_status, name='update_order_status'),
    path('block_user/<int:user_id>',views.block_user, name='block_user'),
]