from products.models import ProductSale


def get_product_sale(product):
    sale = ProductSale.objects.get(product=product).sale
    sale = sale / 100
    sale = sale * product.price
    sale = product.price - sale

    return sale
