from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .create_order_credit import main, is_check_mac_value_match
from .models import Order, Payment
from cart.models import Cart
from django.core import serializers
from django.urls import reverse

# Create your views here.

@login_required
def index(request):
    return render(request, 'order/index.html')

@login_required
@require_POST
def ecpay_view(request):
    the_cart = request.user.cart
    if the_cart.has_invalid():
        return render(request, 'cart/index.html', {'gg_alert': '購物車內有價格異動或缺貨商品！'})
    if not the_cart.cart_product_set.all():
        return render(request, 'cart/index.html', {'gg_alert': '購物車內無商品！'})
    # 建立訂單
    cart_total = the_cart.get_total()
    product_title_list = []

    for the_cart_product in the_cart.cart_product_set.all():
        product_title_list.append(the_cart_product.temp_title)

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

@login_required
@require_POST
def pay_from_index(request):
    order_id = request.POST['order_id']
    queryset = Order.objects.filter(user=request.user)
    the_order = get_object_or_404(queryset, pk=order_id)
    if the_order.has_succeed():
        return render(request, 'order/index.html',{'gg_alert': '這筆訂單已經付款過囉！'})

    the_payment = Payment.objects.create(
        order = the_order,
        trade_no = the_order.generate_trade_no(),
    )
    return HttpResponse(main(the_order.id,request))

@login_required
@require_POST
def cancel(request):
    order_id = request.POST['order_id']
    queryset = Order.objects.filter(user=request.user)
    the_order = get_object_or_404(queryset, pk=order_id)
    alert_msg = '刪除訂單失敗！'
    if the_order.has_succeed():
        alert_msg = '已付款的訂單不能取消！'
        return render(request, 'order/index.html', {'gg_alert': alert_msg})
    if the_order.delete():
        alert_msg = '取消訂單成功！'

    return render(request, 'order/index.html', {'gg_alert': alert_msg})

@csrf_exempt
@require_POST
def result(request):
    post_data = request.POST.dict()
    alert_msg = '交易失敗！'
    if is_check_mac_value_match(post_data):
        if int(post_data['RtnCode']) == 1:
            alert_msg = '交易成功！'
    return render(request, 'redirect.html',{'gg_alert': alert_msg, 'gg_redirect': request.build_absolute_uri(reverse('order:index'))})

@csrf_exempt
def receive_from_ecpay(request):
    post_data = request.POST.dict()
    merchant_trade_no = post_data['MerchantTradeNo']
    if is_check_mac_value_match(post_data):
        try:
            the_payment = Payment.objects.filter(trade_no=merchant_trade_no).get()
            if int(post_data['RtnCode']) == 1:
                the_payment.is_success = True
                the_payment.save()

        except Payment.DoesNotExist:
            print('付款紀錄不存在！')

        return HttpResponse('1|OK')
    else:
        raise Http404("你他媽想搞事？")
