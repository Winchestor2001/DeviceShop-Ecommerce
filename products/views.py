from django.shortcuts import render, redirect
from products.models import ProductSale, ProductPhoto, Product, Review, SavedProduct, MainCategory, ProductCategory, Category, ReviewImage
from accounts.models import Profile
from orders.models import OrderProduct, CartProduct
from datetime import datetime
from django.utils.text import slugify
import markdown

from products.utils import filter_product_reviews, get_product_sale


def product_page(request, id):
    context = {}
    profile = Profile.objects.get(user=request.user)
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        review = Review.objects.create(user=profile, stars=int(request.POST.get('stars')), text=request.POST.get('text'), product=product)
        for photo in request.FILES.getlist('images'):
            ReviewImage.objects.create(image=photo, review=review)
    photo = ProductPhoto.objects.filter(product=product)

    reviews = Review.objects.filter(product=product).order_by('-create_at')

    for_range = range(1, 6)

    review_result = filter_product_reviews(reviews)

    you_may_like_products = Product.objects.filter(main_category=product.main_category)[:10]
    categories = ProductCategory.objects.filter(product=product)
    saved = False
    if SavedProduct.objects.filter(product=product).exists():
        saved = True

    all_photo = []
    for i in photo:
        all_photo.append(i)

    sale = None
    if ProductSale.objects.filter(product=product).exists():
        sale = get_product_sale(product)
    
    markdown_to_html = markdown.markdown(product.description)
    context['markdown_to_html'] = markdown_to_html
    context['product'] = product
    context['photo'] = all_photo
    context['reviews'] = review_result
    context['you_may_like_products'] = you_may_like_products
    context['categories'] = categories
    context['saved'] = saved
    context['range'] = for_range
    context['sale'] = sale
    return render(request, 'product.html', context=context)


def add_to_cart(request, slug):
    profile = Profile.objects.get(user=request.user)
    cart = CartProduct.objects.filter(profile=profile, product__slug=slug)
    product = Product.objects.get(slug=slug)
    if not cart:
        if ProductSale.objects.filter(product=product).exists():
            sale = get_product_sale(product)
            CartProduct.objects.create(product=product, profile=profile, total_price=sale)
        else:
            CartProduct.objects.create(product=product, profile=profile, total_price=product.price)
    else:
        cart_product = cart[0]
        cart_product.quantity += 1
        cart_product.total_price *= cart_product.quantity
        cart_product.save()
    return redirect('cart')


def shop_page(request, category=None):
    if not request.session.get('layout'):
        request.session['layout'] = 1

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

    main_categories = MainCategory.objects.all()

    if main_category == None:
        categories = Category.objects.all()
    else:
        categories = Category.objects.filter(category=main_category)

    sort_by = request.GET.get('sort')
    if sort_by != None:
        if sort_by == 'date_new':
            products_list = products_list.order_by('create_at')
        elif sort_by == 'date_old':
            products_list = products_list.order_by('-create_at')

    active_stars = []
    showing_active_filters = []
    active_brands = []
    active_categories = []
    active_search = ''
    if request.method == 'POST':
        star = 0
        if request.POST.get('star5'):
            star = 5
        elif request.POST.get('star4'):
            star = 4
        elif request.POST.get('star3'):
            star = 3
        elif request.POST.get('star2'):
            star = 2
        elif request.POST.get('star1'):
            star = 1
        min = float(request.POST.get('min'))
        max = float(request.POST.get('max'))
        products_list = products_list.filter(price__gte=min, price__lte=max)
        if star:
            active_stars.append(f'star{star}')
            showing_active_filters.append(f'Star: {star}')
            if star > 1:
                products_list = products_list.filter(stars__gte=star, stars__lt=star+1)
            else:
                products_list = products_list.filter(stars__gte=star-1, stars__lt=star+1)

        for i in brands:
            if request.POST.get(f'brand_{i}'):
                active_brands.append(i)
                showing_active_filters.append(f'Brand: {i}')
        if active_brands:
            products_list = products_list.filter(brand__in=active_brands)

        categories_for_filter = []
        product_categories_for_filter = []
        for i in categories:
            product_categories = ProductCategory.objects.filter(category=i)
            for c in product_categories:
                if request.POST.get(f'{i}_{c.name}'):
                    active_categories.append(f'{i}_{c.name}')
                    showing_active_filters.append(f'{i}: {c.name}')
                    categories_for_filter.append(i)
                    product_categories_for_filter.append(c.name)
        if categories_for_filter:
            products_list = products_list.filter(productcategory__category__in=categories_for_filter, productcategory__name__in=product_categories_for_filter).distinct()
        
        search = request.POST.get('hidden_search')
        if search:
            products_list = products_list.filter(name__icontains=search)
            active_search = search
        
        layout = request.POST.get('layout')
        request.session['layout'] = int(layout)

    products = []
    for i in products_list:
        photo = ProductPhoto.objects.filter(product=i)[0].photo

        orders = OrderProduct.objects.filter(product=i)

        saved = False
        if SavedProduct.objects.filter(product=i).exists():
            saved = True

        sale = None
        if ProductSale.objects.filter(product=i).exists():
            sale = get_product_sale(i)

        rating_list = Review.objects.filter(product=i)
        if rating_list:
            rating = 0
            for s in rating_list:
                rating += s.stars
            rating = round(rating / len(rating_list), 1)
            products.append([i, photo, rating, len(orders), saved, sale])
        else:
            products.append([i, photo, 0.0, len(orders), saved, sale])

    context = {
        'products': products,
        'main_categories': main_categories,
        'current_category': main_category,
        'categories': categories,
        'max_price': int(max_price),
        'min': int(min),
        'max': int(max),
        'brands': brands,
        'sort_by': sort_by,
        'range': range(1, 6),
        'active_stars': active_stars,
        'active_brands': active_brands,
        'active_categories': active_categories,
        'active_search': active_search,
        'showing_active_filters': showing_active_filters,
        'scroll': request.POST.get('scroll', 0)
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
        'sort_by': sort_by,
        'range': range(1, 6)
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
        closest_date_sale = min(products_on_sale, key=lambda x: abs(current_datetime - datetime.combine(x.date, datetime.min.time()))).date
    
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


def change_product_data(request, product_id):
    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        product = Product.objects.get(id=product_id)
        product.name = name
        product.price = price
        product.brand = brand
        product.save()
        return redirect('product', product.id)


def delete_product(request, product_id):
    Product.objects.get(id=product_id).delete()
    return redirect('shop')


def add_discount(request, product_id):
    product = Product.objects.get(id=product_id)
    sale = request.POST.get('discount')
    date = request.POST.get('date')
    ProductSale.objects.create(product=product, sale=sale, date=date)
    return redirect('product', product.id)


def add_product_photos(request, product_id):
    product = Product.objects.get(id=product_id)
    for photo in request.FILES.getlist('product_photos'):
        ProductPhoto.objects.create(photo=photo, product=product)
    return redirect('product', product.id)


def delete_product_sale(request, product_id):
    product = Product.objects.get(id=product_id)
    ProductSale.objects.get(product=product).delete()
    return redirect('product', product.id)