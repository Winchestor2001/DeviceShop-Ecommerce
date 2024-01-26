from django.shortcuts import render, redirect
from .models import OrderProduct, Coupon, CartProduct
from accounts.models import Profile
from products.models import ProductPhoto, ProductCategory
from django.http import JsonResponse, HttpResponse
from django.core.serializers import serialize


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
        else:
            category.append('')
    final_order = zip(all_photo, orders_in_cart, category)
    context['len_cart'] = len(orders_in_cart)
    context['orders'] = final_order

    return render(request, 'cart.html', context=context)


def delete_cart(request, cart_id):
    CartProduct.objects.get(profile__user=request.user, id=cart_id).delete()
    return redirect("cart")


def delete_all_cart(request):
    CartProduct.objects.filter(profile__user=request.user).delete()
    return redirect("cart")


def update_quantity(request):
    product_id = request.GET.get('product_id')
    action = request.GET.get('action')
    response_data = {'id': product_id, 'Action': action}
    cart_product = CartProduct.objects.get(profile__user=request.user, product__id=product_id)
    if action == 'plus':
        cart_product.quantity += 1
    if action == 'minus':
        cart_product.quantity -= 1
    cart_product.save()
    return JsonResponse(response_data)


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
