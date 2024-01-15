from products.models import ReviewImage


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
