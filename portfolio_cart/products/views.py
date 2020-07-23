from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from .models import Product
from urllib.parse import unquote

def index(request):
    return render(request, 'products/index.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': product, 'stock_range': range(1, product.stock+1)})


def cat(request, product_cat):
    unquoted_cat = unquote(product_cat)
    products = list(Product.objects.filter(cat=unquoted_cat))
    page_title = "分類:" + unquoted_cat
    return render(request, 'products/products.html', {'products': products, 'page_title': page_title})

def search(request):
    keyword = request.GET['keyword']
    products = list(Product.objects.filter(title__icontains=keyword))
    page_title = "搜尋 \"" + keyword + "\" 的結果"
    return render(request, 'products/products.html', {'products': products, 'page_title': page_title})
