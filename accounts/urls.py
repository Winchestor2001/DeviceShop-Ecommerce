from django.urls import path
from .views import *

urlpatterns = [
    path('account/<str:username>', account_page, name='account'),
    path('individual_profiles/', individual_profiles, name='indiv_profile'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('forgot_password/', forgot_password_page, name='forgot_password'),
    path('change_password/', change_password_page, name='change_password'),
]