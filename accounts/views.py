from django.shortcuts import render


def account_page(request):
    return render(request, 'account.html')

def login_page(request):
    return render(request, 'login.html')

def register_page(request):
    return render(request, 'register.html')