from django.shortcuts import render, redirect
from .models import OrderProduct, Coupon
from accounts.models import Profile
from products.models import ProductPhoto
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize


def cart_page(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    orders_in_cart = OrderProduct.objects.filter(user=profile)
    all_photo = []
    for product in orders_in_cart:
        photo = ProductPhoto.objects.filter(product=product.product)
        for p in photo:
            all_photo.append(p)
    final_order = zip(all_photo, orders_in_cart)
    context['orders'] = final_order
    return render(request, 'cart.html', context=context)


def checkout_page(request):
    return render(request, 'checkout.html')

def check_coupon(request):
    if request.method == 'GET':
        coupon = Coupon.objects.filter(code=request.GET.get('coupon'))
        if coupon.exists():
            data = serialize('json', coupon)
            return JsonResponse(data, safe=False)
        else:
            return HttpResponse(None)