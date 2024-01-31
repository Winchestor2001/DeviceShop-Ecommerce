from django.shortcuts import render, redirect
from .models import Coupon, CartProduct, City, PickUp, Order, OrderProduct
from accounts.models import Profile
from products.models import ProductPhoto, ProductCategory, Product
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
    final_order = zip(all_photo, orders_in_cart)
    context['len_cart'] = len(orders_in_cart)
    context['orders'] = final_order
    context['category'] = category

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
    product = Product.objects.get(id=product_id)
    cart_product = CartProduct.objects.get(profile__user=request.user, product__id=product_id)
    if action == 'plus':
        cart_product.quantity += 1
        cart_product.total_price += product.price
    if action == 'minus':
        cart_product.quantity -= 1
        cart_product.total_price -= product.price
    cart_product.save()
    return JsonResponse(response_data)


def checkout_page(request):
    context = {}
    orders_photo = []
    total_order_price = []
    total = 0
    shipping = 10.00

    citys = City.objects.all()
    profile = Profile.objects.get(user=request.user)
    orders = CartProduct.objects.filter(profile=profile)

    for product in orders:
        photo = ProductPhoto.objects.get(product=product.product)
        orders_photo.append(photo)
        total_price = product.quantity*product.product.price
        total_order_price.append(total_price)
        total += total_price

    if request.GET:
        city = request.GET.get('city')
        pick_ups = PickUp.objects.filter(city__city=city)
        data = serialize('json', pick_ups)
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        city = request.POST.get('city')
        pick_up = request.POST.get('pick_up')

        order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, phone_number=phone,
                             city='tashkent', pick_up='pick up N1', total_price=total, user=profile)

        for item in orders:
            OrderProduct.objects.create(
                product=item.product,
                user=profile,
                order=order,
                quantity=item.quantity
            )

        orders.delete()
        return redirect('account', username=profile.user.username)

    final_orders = zip(orders, orders_photo, total_order_price)
    context['city'] = citys
    context['orders'] = final_orders
    context['total'] = total
    context['shipping'] = shipping

    return render(request, 'checkout.html', context=context)


def check_coupon(request):
    if request.method == 'GET':
        coupon = Coupon.objects.filter(code=request.GET.get('coupon'))
        if coupon.exists():
            data = serialize('json', coupon)
            return JsonResponse(data, safe=False)
        else:
            return HttpResponse(None)
