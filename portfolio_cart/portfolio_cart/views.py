from django.shortcuts import render
from products.models import Product
from django.urls import reverse

def index(request):
    latest_products = Product.objects.order_by('-datetime_create')[:8]
    feature_products = Product.objects.filter(is_feature_product=True)[:8]
    context = {
        'latest_products' : latest_products,
        'feature_products' : feature_products,
    }

    return render(request, 'index.html', context)

def about(request):
    return render(request, 'about.html')