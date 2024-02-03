from django.urls import path
from .views import *

urlpatterns = [
    path('account/<str:username>', account_page, name='account'),
    path('individual_profiles/', individual_profiles, name='indiv_profile'),
    path('seller_profile/<str:username>', seller_profile_page, name='seller_profile'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('forgot_password/', forgot_password_page, name='forgot_password'),
    path('change_password/<str:id>', change_password_page, name='change_password'),
    path('cancel_order/<int:order_id>/', cancel_order, name='cancel_order')
]