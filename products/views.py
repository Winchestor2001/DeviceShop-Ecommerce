from django.shortcuts import render, redirect
from products.models import ProductSale, ProductPhoto, Product, Review, SavedProduct, MainCategory, ProductCategory, Category, ReviewImage
from accounts.models import Profile
from orders.models import OrderProduct, CartProduct
from datetime import datetime
from django.utils.text import slugify
import markdown

from products.utils import filter_product_reviews


def product_page(request, slug):
    context = {}
    profile = Profile.objects.get(user=request.user)
    product = Product.objects.get(slug=slug)
    if request.method == 'POST':
        review = Review.objects.create(user=profile, stars=int(request.POST.get('stars')), text=request.POST.get('text'), product=product)
        for photo in request.FILES.getlist('images'):
            ReviewImage.objects.create(image=photo, review=review)
    photo = ProductPhoto.objects.filter(product=product)

    reviews = Review.objects.filter(product=product).order_by('-create_at')

    
    stars = 0
    for i in reviews:
        stars += int(i.stars)
    stars = stars / len(reviews)
    stars = [round(stars, 1), range(5)]

    review_result = filter_product_reviews(reviews)

    you_may_like_products = Product.objects.filter(main_category=product.main_category)[:10]
    categories = ProductCategory.objects.filter(product=product)
    saved = False
    if SavedProduct.objects.filter(product=product).exists():
        saved = True

    all_photo = []
    for i in photo:
        all_photo.append(i)
    
    markdown_to_html = markdown.markdown(product.description)
    context['markdown_to_html'] = markdown_to_html
    context['product'] = product
    context['photo'] = all_photo
    context['reviews'] = review_result
    context['you_may_like_products'] = you_may_like_products
    context['categories'] = categories
    context['saved'] = saved
    context['stars'] = stars
    return render(request, 'product.html', context=context)


def add_to_cart(request, slug):
    profile = Profile.objects.get(user=request.user)
    cart = CartProduct.objects.filter(profile=profile, product__slug=slug)
    product = Product.objects.get(slug=slug)
    if not cart:
        CartProduct.objects.create(product=product, profile=profile)
    else:
        cart[0].quantity += 1
        cart[0].save()
    return redirect('cart')


def shop_page(request, category=None):
    main_category = None
    if category == None:
        products_list = Product.objects.all()
        brands = Product.objects.values_list('brand', flat=True).distinct()
    else:
        main_category = MainCategory.objects.get(slug=category)
        products_list = Product.objects.filter(main_category=main_category).distinct()
        brands = Product.objects.filter(main_category=main_category).values_list('brand', flat=True).distinct()

    if products_list.exists():
        if category == None:
            max_price = Product.objects.order_by('price').last().price
        else:
            max_price = Product.objects.filter(main_category=main_category).order_by('price').last().price
    else:
        max_price = 0

    min = 0
    max = max_price

    if request.method == 'POST':
        min = float(request.POST.get('min'))
        max = float(request.POST.get('max'))
        products_list = products_list.filter(price__gte=min, price__lte=max)

    sort_by = request.GET.get('sort')
    if sort_by != None:
        if sort_by == 'date_new':
            products_list = products_list.order_by('create_at')
        elif sort_by == 'date_old':
            products_list = products_list.order_by('-create_at')

    products = []
    for i in products_list:
        photo = ProductPhoto.objects.filter(product=i)[0].photo

        orders = OrderProduct.objects.filter(product=i)

        saved = False
        if SavedProduct.objects.filter(product=i).exists():
            saved = True

        rating_list = Review.objects.filter(product=i)
        if rating_list:
            rating = 0
            for s in rating_list:
                rating += s.stars
            rating = rating / len(rating_list)
            products.append([i, photo, rating, len(orders), saved])
        else:
            products.append([i, photo, "0 Reviews", len(orders), saved])

    main_categories = MainCategory.objects.all()

    if main_category == None:
        categories = Category.objects.all()
    else:
        categories = Category.objects.filter(category=main_category)

    context = {
        'products': products,
        'main_categories': main_categories,
        'current_category': main_category,
        'categories': categories,
        'max_price': max_price,
        'min': min,
        'max': max,
        'brands': brands,
        'sort_by': sort_by,
        'range': range(1, 6)
    }
    return render(request, 'shop.html', context=context)


def saved_page(request, category=None):
    main_category = None
    profile = Profile.objects.get(user=request.user)
    if category == None:
        products_list = SavedProduct.objects.filter(user=profile)
        brands = SavedProduct.objects.filter(user=profile).values_list('product__brand', flat=True).distinct()
    else:
        main_category = MainCategory.objects.get(slug=category)
        products_list = SavedProduct.objects.filter(product__main_category=main_category, user=profile).distinct()
        brands = SavedProduct.objects.filter(product__main_category=main_category, user=profile).values_list('product__brand', flat=True).distinct()

    sort_by = request.GET.get('sort')
    if sort_by != None:
        if sort_by == 'date_new':
            products_list = products_list.order_by('product__create_at')
        elif sort_by == 'date_old':
            products_list = products_list.order_by('-product__create_at')

    products = []
    for i in products_list:
        photo = ProductPhoto.objects.filter(product=i.product)[0].photo

        orders = OrderProduct.objects.filter(product=i.product)

        saved = False
        if SavedProduct.objects.filter(product=i.product).exists():
            saved = True

        rating_list = Review.objects.filter(product=i.product)
        if rating_list:
            rating = 0
            for s in rating_list:
                rating += s.stars
            rating = rating / len(rating_list)
            products.append([i.product, photo, [rating, range(round(rating))], len(orders), saved])
        else:
            products.append([i.product, photo, ["0 Reviews", range(round(0))], len(orders), saved])

    main_categories = MainCategory.objects.all()

    if main_category == None:
        categories = Category.objects.all()
    else:
        categories = Category.objects.filter(category=main_category)

    if products_list.exists():
        if category == None:
            max_price = SavedProduct.objects.order_by('product__price').last().product.price
        else:
            max_price = SavedProduct.objects.filter(product__main_category=main_category).order_by('product__price').last().product.price
    else:
        max_price = 0

    context = {
        'products': products,
        'main_categories': main_categories,
        'current_category': main_category,
        'categories': categories,
        'max_price': max_price,
        'brands': brands,
        'sort_by': sort_by
    }
    return render(request, 'saved.html', context=context)


def save_product(request, id):
    product = Product.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    saved_product = SavedProduct.objects.filter(product=product)
    if saved_product.exists():
        saved_product.delete()
    else:
        SavedProduct.objects.create(product=product, user=profile)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def add_product_page(request):
    main_categories = MainCategory.objects.all()
    main_category = MainCategory.objects.first()
    if request.POST:
        main_category_input = request.POST.get('main_category')
        main_category = MainCategory.objects.get(name=main_category_input)
    context = {
        'main_categories': main_categories,
        'main_category': main_category,
        'categories': Category.objects.filter(category=main_category)
    }
    return render(request, 'addproduct.html', context=context)


def add_product(request):
    if request.method == 'POST':
        main_category = request.POST.get('hidden_main_category')
        main_category = MainCategory.objects.get(name=main_category)
        categories = Category.objects.filter(category=main_category)
        name = request.POST.get('name')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        supplier = Profile.objects.get(user=request.user)
        description = request.POST.get('description')
        state = request.POST.get('state')
        product = Product.objects.create(slug=slugify(name), name=name, price=price, brand=brand, supplier=supplier, description=description, state=state, main_category=main_category)
        for photo in request.FILES.getlist('images'):
            ProductPhoto.objects.create(photo=photo, product=product)
        for i in categories:
            category_name = request.POST.get(f'{i}')
            ProductCategory.objects.create(product=product, category=i, name=category_name)
    return redirect('addproductpage')


def home_page(request):
    main_categories_obj = MainCategory.objects.all()
    main_categories = []
    for i in main_categories_obj:
        price = 0
        if Product.objects.filter(main_category=i).exists():
            price = Product.objects.filter(main_category=i).order_by('price')[0].price
        main_categories.append([i, price])
    
    products_on_sale = ProductSale.objects.all()[:5]
    products_on_sale_list = []
    for i in products_on_sale:
        photo = ProductPhoto.objects.get(product=i.product).photo
        products_on_sale_list.append([i, photo])

    current_datetime = datetime.now()
    closest_date_sale = "January 1, 2025 00:00:00"
    if len(products_on_sale) > 0:
        closest_date_sale = min(products_on_sale, key=lambda x: abs(current_datetime - x.date))
    
    products_list = Product.objects.all()[:8]
    products = []
    for i in products_list:
        photo = ProductPhoto.objects.filter(product=i)[0].photo
        products.append([i, photo])

    context = {
        'main_categories': main_categories,
        'products_on_sale': products_on_sale_list,
        'closest_date_sale': closest_date_sale,
        'products': products
    }
    return render(request, 'index.html', context=context)