from django.urls import path
from .views import *

urlpatterns = [
    path('product/<int:id>', product_page, name='product'),
    path('shop/<str:category>', shop_page, name='category_shop'),
    path('shop/', shop_page, name='shop'),
    path('saved/', saved_page, name='saved'),
    path('saved/<str:category>', saved_page, name='category_saved'),
    path('save_product/<int:id>', save_product, name='save_product'),
    path('add_product/', add_product_page, name='addproductpage'),
    path('addproduct/', add_product, name='addproduct'),
    path('', home_page, name='home'),
    path('add_to_cart/<slug:slug>', add_to_cart, name='add_to_cart'),
    path('change_product_data/<int:product_id>', change_product_data, name='change_product_data'),
    path('delete_product/<int:product_id>', delete_product, name='delete_product'),
    path('add_discount/<int:product_id>', add_discount, name='add_discount'),
    path('add_product_photos/<int:product_id>', add_product_photos, name='add_product_photos'),
    path('delete_sale/<int:product_id>', delete_product_sale, name='delete_product_sale'),
]