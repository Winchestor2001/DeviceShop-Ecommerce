from products.models import ReviewImage, ProductSale


def filter_product_reviews(reviews):
    review_data = []

    for item in reviews:
        images = ReviewImage.objects.filter(review=item)
        review_data.append(
            {
                "review": item,
                "images": images
            }
        )
    return review_data


def get_product_sale(product):
    sale = ProductSale.objects.get(product=product).sale
    sale = sale / 100
    sale = sale * product.price
    sale = product.price - sale

    return sale
