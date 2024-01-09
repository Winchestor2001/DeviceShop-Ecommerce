from django.shortcuts import render
from categories.models import MainCategory, ProductCategory
from products.models import ProductSale, ProductPhoto
from datetime import datetime


def product_page(request):
    return render(request, 'product.html')

def shop_page(request):
    return render(request, 'shop.html')

def saved_page(request):
    return render(request, 'saved.html')

def home_page(request):
    main_categories = MainCategory.objects.all()

    products_on_sale = ProductSale.objects.all()[:5]
    products_on_sale_list = []
    for i in products_on_sale:
        photo = ProductPhoto.objects.get(product=i.product).photo
        products_on_sale_list.append([i, photo])

    current_datetime = datetime.now()
    closest_date_sale = "January 1, 2025 00:00:00"
    if len(products_on_sale) > 0:
        closest_date_sale = min(products_on_sale, key=lambda x: abs(current_datetime - x.date))
    
    products_list = ProductCategory.objects.all()[:8]
    products = []
    for i in products_list:
        photo = ProductPhoto.objects.get(product=i.product).photo
        products.append([i, photo])

    context = {
        'main_categories': main_categories,
        'products_on_sale': products_on_sale_list,
        'closest_date_sale': closest_date_sale,
        'products': products
    }
    return render(request, 'index.html', context=context)