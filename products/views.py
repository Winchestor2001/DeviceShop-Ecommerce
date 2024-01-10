from django.shortcuts import render, redirect
from categories.models import MainCategory, ProductCategory, Category
from products.models import ProductSale, ProductPhoto, Product, Review
from accounts.models import Profile
from orders.models import OrderProduct
from datetime import datetime


def product_page(request):
    return render(request, 'product.html')

def shop_page(request, category=None):
    if category == None:
        products_list = Product.objects.all()
    else:
        main_category = MainCategory.objects.get(slug=category)
        not_unique_products_list = Product.objects.filter(productcategory__category__category=main_category)
        products_list = []
        for item in not_unique_products_list:
            if item not in products_list:
                products_list.append(item)
    products = []
    for i in products_list:
        photo = ProductPhoto.objects.filter(product=i)[0].photo

        orders = OrderProduct.objects.filter(product=i)

        rating_list = Review.objects.filter(product=i)
        if rating_list:
            rating = 0
            for i in rating_list:
                rating += i.stars
            rating = rating / len(rating_list)
            products.append([i, photo, [rating, range(round(rating))], len(orders)])
        else:
            products.append([i, photo, ["0 Reviews", range(round(0))], len(orders)])

    main_categories = MainCategory.objects.all()

    context = {
        'products': products,
        'main_categories': main_categories,
    }
    return render(request, 'shop.html', context=context)

def saved_page(request):
    return render(request, 'saved.html')

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
        name = request.POST.get('name')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        supplier = Profile.objects.get(user=request.user)
        description = request.POST.get('description')
        state = request.POST.get('state')
        product = Product.objects.create(name=name, price=price, brand=brand, supplier=supplier, description=description, state=state)
        for photo in request.FILES.getlist('images'):
            ProductPhoto.objects.create(photo=photo, product=product)
        main_category = request.POST.get('hidden_main_category')
        main_category = MainCategory.objects.get(name=main_category)
        categories = Category.objects.filter(category=main_category)
        for i in categories:
            category_name = request.POST.get(f'{i}')
            ProductCategory.objects.create(product=product, category=i, name=category_name)
    return redirect('addproductpage')

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