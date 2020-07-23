import importlib.util
from .models import Order
import pathlib

current_path = str(pathlib.Path(__file__).parent.absolute())
# 第一個需要修改的，就是 SDK 路徑
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",  # SDK檔名不用改
    current_path+"/ecpay_payment_sdk.py"  # 改成 django app name/sdk name，
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

from django.urls import reverse
from datetime import datetime

def main(order_id,request):

    #從新建的order取出資料
    the_order = Order.objects.get(pk=order_id)
    the_payment = the_order.payment_set.latest()

    # 第二個需要修改的，商品資訊
    order_params = {
        'MerchantTradeNo': the_payment.trade_no,
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': the_order.total_amount,  # 商品金額
        'TradeDesc': '私密好物販售',  # 商品描述
        'ItemName': the_order.product_title,  # 商品名稱，用井字號當分行
        'ReturnURL': request.build_absolute_uri(reverse('order:receive_from_ecpay')),  # 顧客填完付款資料後的跳轉頁面
        'ChoosePayment': 'Credit',  # 顧客的付費方式

        # 結帳後，先導到 OrderResultURL，從綠界頁面跳回的頁面
        # 如果沒有參數才會跳轉到 ClientBackURL
        'ClientBackURL': request.build_absolute_uri(reverse('order:result')), # 或是交易失敗時的「返回商店」連結也會導到這裡
        'ItemURL': '',  # 商品資訊頁面
        'Remark': '交易備註',  # 備註文字
        'ChooseSubPayment': '',

        # 結帳成功/失敗後的結果頁面，告知顧客本次的結帳結果
        'OrderResultURL': request.build_absolute_uri(reverse('order:result')),
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }

    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 2,
    }

    # 發票資訊
    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )

    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)

    # 合併發票參數
    order_params.update(inv_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)
        checkMacValue = final_order_params['CheckMacValue']
        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        # 最後產出 html，回傳回去顯示此 html
        return html
    except Exception as error:
        print('An exception happened: ' + str(error))

def is_check_mac_value_match(params):
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )
    check_mac_value = params.pop('CheckMacValue')
    if check_mac_value == ecpay_payment_sdk.generate_check_value(params):
        return True

    return False