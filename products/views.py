from django.shortcuts import render


def product_page(request):
    return render(request, 'product.html')

def shop_page(request):
    return render(request, 'shop.html')

def saved_page(request):
    return render(request, 'saved.html')

def home_page(request):
    return render(request, 'index.html')