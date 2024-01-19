from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', cart_page, name='cart'),
    path('checkout/', checkout_page, name='checkout'),
    path('check_coupon/', check_coupon, name='check_coupon'),
]