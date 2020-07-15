from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .create_order_credit import main
from .models import Order, Payment
from cart.models import Cart
from django.core import serializers


# Create your views here.

@csrf_exempt
def ecpay_view(request):
    #建立訂單
    cart_total = request.user.cart.get_total()
    product_title_list = []
    for the_cart_product in request.user.cart.cart_product_set.all():
        product_title_list.append(the_cart_product.temp_title)

    titles_with_sharp = '#'.join(product_title_list)
    the_serialized_cart = serializers.serialize("json", request.user.cart.cart_product_set.all())
    the_order = Order.objects.create(
        user = request.user,
        serialized_cart = the_serialized_cart,
        total_amount = cart_total,
        product_title = titles_with_sharp,
    )
    the_payment = Payment.objects.create(
        order = the_order,
        trade_no = the_order.generate_trade_no(),
    )
    #create order with cart
    #create payment
    return HttpResponse(main(the_order.id))

def result(request):
    return HttpResponse('nothing here.(result)')

def detail(request):
    return HttpResponse('nothing here.(detail)')

@csrf_exempt
def receive_from_ecpay(request):
    print('進入view了')
    trade_no = request.POST['MerchantTradeNo']
    try:
        the_payment = Payment.objects.filter(check_mac_value=request.POST['CheckMacValue'])
        the_payment.is_success = True
        print('交易成功！')
    except Payment.DoesNotExist:
        print('付款紀錄不存在！')

    return HttpResponse('1|OK')