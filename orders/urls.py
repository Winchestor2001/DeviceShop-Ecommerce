from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', cart_page, name='cart'),
    path('checkout/', checkout_page, name='checkout'),
    path('ajax/update_quantity/', update_quantity, name="update_quantity"),
]