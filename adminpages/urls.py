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
    path('coupons/',views.coupons, name='coupons'),
    path('add_coupon/',views.add_coupon, name='add_coupon'),
    path('offers_list/',views.offers_list, name='offers_list'),
    path('add_offer/',views.add_offer, name='add_offer'),
    path('report/',views.report, name='report'),
    path('sales_report_pdf/', views.sales_report_pdf, name='sales_report_pdf'),
    path('sales_report_excel/',  views.sales_report_excel, name='sales_report_excel'),
    path('brands/',  views.brands, name='brands'),
    path('add_brand/',  views.add_brand, name='add_brand')
    
]
