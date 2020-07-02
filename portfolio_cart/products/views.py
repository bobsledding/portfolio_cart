from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Product

def index(request):
    return render(request, 'products/index.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html', {'product': product})