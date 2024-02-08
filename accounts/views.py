from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

from orders.models import OrderProduct, Order
from orders.utils import get_product_sale
from products.models import ProductPhoto, Product, SavedProduct, Review, ProductSale
from accounts.models import Profile, ResetPassword
from .utils import send_gmail


def account_page(request, username):
    context = {}
    if not request.user.is_authenticated:
        return redirect('login')

    profile = Profile.objects.get(user__username=username)
    user_data = User.objects.get(profile=profile)
    orders = Order.objects.filter(user=profile).order_by('-create_at')

    result_order = []
    product_price = []
    images = []

    for order in orders:
        products_in_order = OrderProduct.objects.filter(order=order)
        products = [item for item in products_in_order]
        result_order.append(products)

        for order_item in products_in_order:
            product = order_item.product

            if ProductSale.objects.filter(product=product).exists():
                sale = get_product_sale(product)
                product_price.append(order_item.quantity * sale)
            else:
                product_price.append(order_item.quantity * order_item.product.price)
            product_photo = ProductPhoto.objects.filter(product=product)[0].photo
            images.append(product_photo)

    if request.method == "POST":
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if request.FILES:
            file_obj = request.FILES['photo']
            filename = f"profile/{username}_{file_obj}"
            with default_storage.open(filename, 'wb+') as d:
                for chunk in file_obj.chunks():
                    d.write(chunk)
                profile.photo = filename
            profile.save()
            return redirect('account', username=username)

        if email:
            if not email.endswith("@gmail.com"):
                email = f"{email}@gmail.com"
            profile.user.email = email
        if phone_number:
            if len(phone_number) == 13 and phone_number.startswith('+998'):
                profile.phone_number = phone_number
            else:
                context['error'] = 'Error phone number! Please write again.'
        if password:
            if len(password) >= 8:
                user_data.password = make_password(password)
            else:
                context['error'] = 'Password must be at least 8 characters!'
    profile.save()
    user_data.save()

    order_data = zip(orders, result_order, product_price, images)
    context['profile'] = profile
    context['order_data'] = order_data
    context['len_orders'] = len(orders)

    return render(request, 'account.html', context=context)


def individual_profiles(request):
    user = User.objects.get(profile__user=request.user)
    context = {'user': user}
    return render(request, 'header.html', context=context)


def cancel_order(request, order_id):
    Order.objects.get(user__user=request.user, id=order_id).delete()
    return redirect('account', username=request.user.username)


def seller_profile_page(request, username):
    context = {}
    profile = Profile.objects.get(user__username=username)
    product = Product.objects.filter(supplier=profile)
    user_products = []
    for i in product:
        product_photo = ProductPhoto.objects.filter(product=i)[0].photo

        saved = False
        if SavedProduct.objects.filter(product=i).exists():
            saved = True

        rating_list = Review.objects.filter(product=i)
        if rating_list:
            rating = 0
            for s in rating_list:
                rating += s.stars
            rating = round(rating / len(rating_list), 1)
            user_products.append([i, product_photo, rating, saved])
        else:
            user_products.append([i, product_photo, 0.0, saved])
    context['user_products'] = user_products
    context['profile'] = profile
    context['range'] = range(1, 6)

    return render(request, 'seller_profile.html', context=context)


def login_page(request):
    if not request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            context = {
                "username": username,
                "password": password
            }
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                context['error'] = "Incorrect username or password"
        return render(request, "login.html", context=context)
    else:
        return redirect("home")


def register_page(request):
    if not request.user.is_authenticated:
        context = {}
        if request.method == "POST":
            username = request.POST.get('username')
            password1 = request.POST.get('password')
            password2 = request.POST.get('repeat_password')
            email = request.POST.get('email')
            terms = request.POST.get('terms')
            context = {
                'username': username,
                'password': password1,
                'repeat_password': password2,
                'email': email
            }
            if len(password1) >= 8:
                if not User.objects.filter(email=email).exists():
                    if not username.isdigit():
                        if not User.objects.filter(username=username).exists():
                            if password1 == password2:
                                if terms != None:
                                    user = User.objects.create_user(
                                        username=username, password=password1, email=email
                                    )
                                    Profile.objects.create(
                                        user=user
                                    )
                                    login(request, user)
                                    return redirect("home")
                                else:
                                    context['error'] = "You must confirm our terms and conditions"
                            else:
                                context['error'] = "Passwords don't match"
                        else:
                            context['error'] = "Username already taken"
                    else:
                        context['error'] = "Username mustn't contain only numbers"
                else:
                    context['error'] = "Email already taken"
            else:
                context['error'] = "Password must be at least 8 characters"
        return render(request, "register.html", context=context)
    else:
        return redirect('home')


def logout_page(request):
    logout(request)
    return redirect('login')


def forgot_password_page(request):
    context = {}
    if request.method == 'POST':
        error = send_gmail(request.POST.get('email'))
        if error:
            context['error'] = error
    return render(request, 'forgot_password.html', context=context)


def change_password_page(request, id):
    context = {}
    if request.method == 'POST':
        if ResetPassword.objects.filter(url=id).exists():
            password1 = request.POST.get('password')
            password2 = request.POST.get('repeat_password')
            if len(password1) >= 8:
                if password1 == password2:
                    user = ResetPassword.objects.get(url=id).user
                    user.set_password(password1)
                    user.save()
                    return redirect('login')
                else:
                    context['error'] = "Passwords don't match"
            else:
                context['error'] = "Password must be at least 8 characters"
    return render(request, 'change_password.html', context=context)