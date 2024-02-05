from django.urls import path

from .views import *

urlpatterns = [
    path('cart/', cart_page, name='cart'),
    path('checkout/', checkout_page, name='checkout'),
    path('ajax/update_quantity/', update_quantity, name="update_quantity"),
    path('delete_cart/<int:cart_id>/', delete_cart, name="delete_cart"),
    path('delete_all_cart/', delete_all_cart, name="delete_all_cart"),
    path('check_coupon/', check_coupon, name='check_coupon'),
]