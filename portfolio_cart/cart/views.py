from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, Cart_product

# Create your views here.

def index(request):
    return render(request, 'cart/index.html')

@require_POST
def add_to_cart(request):

    product_id = request.POST['product_id']
    quantity = int(request.POST['quantity'])
    user_cart = request.user.cart
    the_cart_product = None
    response_dict = {
        'message' : '',
        'success' : 0,
    }
    # 檢查該商品是否存在.
    the_product = None
    try:
        the_product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        response_dict['message'] = '此商品不存在！'
        return JsonResponse(response_dict)

    if the_product in user_cart.products.all():
        the_cart_product = Cart_product.objects.get(cart=user_cart, product=the_product)
        # 檢查購物車總商品數量是否<=商品庫存
        if the_cart_product.quantity + quantity > the_product.stock :
            response_dict['message'] = '庫存不足！'
            return JsonResponse(response_dict)
    else:
        # 若無，新增cart_product
        the_cart_product = Cart_product(
            cart=user_cart,
            product=the_product,
        )
    # 檢查完，加入購物車。
    the_cart_product.temp_title = the_product.title
    the_cart_product.temp_price = the_product.price
    the_cart_product.quantity += quantity
    the_cart_product.save()

    # return message
    response_dict['message'] = the_product.title + ' ' + str(quantity) + '個 已加入購物車！'
    response_dict['success'] = 1

    return JsonResponse(response_dict)

@require_POST
def remove_from_cart(request):

    user_cart = request.user.cart
    cpid = int(request.POST['cpid'])
    response_dict = {
        'success' : 0,
    }
    if user_cart.cart_product_set.filter(pk=cpid).exists():
        the_cart_product = Cart_product.objects.get(pk=cpid)
        the_product = the_cart_product.product
        user_cart.products.remove(the_product)
        response_dict['success'] = 1

    return JsonResponse(response_dict)