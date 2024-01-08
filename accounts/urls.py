from django.urls import path
from .views import *

urlpatterns = [
    path('account/', account_page, name='account'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
]