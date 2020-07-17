from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .create_order_credit import main, is_check_mac_value_match
from .models import Order, Payment
from cart.models import Cart
from django.core import serializers
from django.db.models import F

# Create your views here.

def ecpay_view(request):
    the_cart = request.user.cart
    if the_cart.has_invalid():
        return render(request, 'cart/index.html', {'gg_alert': '購物車內有價格異動或缺貨商品！'})
    # 建立訂單
    cart_total = the_cart.get_total()
    product_title_list = []

    for the_cart_product in the_cart.cart_product_set.all():
        product_title_list.append(the_cart_product.temp_title)
        the_product = the_cart_product.product
        the_product.stock = F('stock') - the_cart_product.quantity
        the_product.save()

    titles_with_sharp = '#'.join(product_title_list)
    the_serialized_cart = serializers.serialize("json", the_cart.cart_product_set.all())
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
    # clear cart
    the_cart.clear_cart()

    return HttpResponse(main(the_order.id,request))

@csrf_exempt
def result(request):
    return HttpResponse('' + request.POST['RtnMsg']+'____'+request.POST['CheckMacValue'])

def index(request):

    orders = request.user.order_set.all()
    return render(request, 'order/index.html', {'orders': orders})

@csrf_exempt
def receive_from_ecpay(request):
    print('進入view了')
    post_data = request.POST.dict()
    merchant_trade_no = post_data['MerchantTradeNo']
    if is_check_mac_value_match(post_data):
        try:
            the_payment = Payment.objects.filter(trade_no=merchant_trade_no).get()
            if int(post_data['RtnCode']) == 1:
                the_payment.is_success = True
                the_payment.save()
                print('交易成功！')

        except Payment.DoesNotExist:
            print('付款紀錄不存在！')

        return HttpResponse('1|OK')
    else:
        raise Http404("你他媽想搞事？")

