from django.shortcuts import render
from .models import CartProduct
from accounts.models import Profile
from products.models import ProductPhoto, ProductCategory
from django.http import HttpResponse


def cart_page(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    orders_in_cart = CartProduct.objects.filter(profile=profile)
    all_photo = []
    category = []
    for product in orders_in_cart:
        photo = ProductPhoto.objects.filter(product=product.product)
        categories = ProductCategory.objects.filter(product=product.product)
        for p in photo:
            all_photo.append(p)
        for c in categories:
            category.append(c)
    final_order = zip(all_photo, orders_in_cart)
    context['orders'] = final_order
    context['category'] = category

    return render(request, 'cart.html', context=context)


def update_quantity(request):
    quantity_id = request.GET.get('quantity_id')
    action = request.POST.get('action')
    print(quantity_id)
    return


def checkout_page(request):
    return render(request, 'checkout.html')