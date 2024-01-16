from django.urls import path
from .views import *

urlpatterns = [
    path('product/<slug:slug>', product_page, name='product'),
    path('shop/<str:category>', shop_page, name='category_shop'),
    path('shop/', shop_page, name='shop'),
    path('saved/', saved_page, name='saved'),
    path('saved/<str:category>', saved_page, name='category_saved'),
    path('save_product/<int:id>', save_product, name='save_product'),
    path('add_product/', add_product_page, name='addproductpage'),
    path('addproduct/', add_product, name='addproduct'),
    path('', home_page, name='home'),
    path('add_to_cart/<slug:slug>', add_to_cart, name='add_to_cart'),
]