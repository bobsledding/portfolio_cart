from .models import Product

def get_product_cats(request):
    product_cats = []
    for cat in Product.objects.values_list('cat', flat=True).distinct():
        product_cats.append(cat)
    return {
        'product_cats' : product_cats,
    }