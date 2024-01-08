from django.urls import path
from .views import *

urlpatterns = [
    path('product/', product_page, name='product'),
    path('shop/', shop_page, name='shop'),
    path('saved/', saved_page, name='saved'),
]