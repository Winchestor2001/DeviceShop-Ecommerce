from django.urls import path
from .views import *

urlpatterns = [
    path('product/', product_page, name='product'),
    path('shop/<str:category>', shop_page, name='category_shop'),
    path('shop/', shop_page, name='shop'),
    path('saved/', saved_page, name='saved'),
    path('add_product/', add_product_page, name='addproductpage'),
    path('addproduct/', add_product, name='addproduct'),
    path('', home_page, name='home'),
]