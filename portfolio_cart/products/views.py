from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import Product

def index(request):
    return render(request, 'products/index.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})


def cat(request, product_cat):
    products = list(Product.objects.filter(cat=product_cat))
    return render(request, 'products/products.html', {'products': products})

def search(request):
    keyword = request.GET['keyword']
    products = list(Product.objects.filter(title__icontains=keyword))
    return render(request, 'products/products.html', {'products': products})
