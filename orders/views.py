from django.shortcuts import render


def cart_page(request):
    return render(request, 'cart.html')

def checkout_page(request):
    return render(request, 'checkout.html')