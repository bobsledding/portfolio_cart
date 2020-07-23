from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core import serializers
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.db.models import F

class Order(models.Model):
    class Meta:
        ordering = ['-datetime_create']

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_create = models.DateTimeField('建立日期',auto_now_add=True)
    datetime_edit = models.DateTimeField('修改日期',auto_now=True)
    serialized_cart = models.TextField('序列化的購物車')
    total_amount = models.PositiveIntegerField('總價')
    product_title = models.TextField('商品名以#分隔')
    datetime_create = models.DateTimeField('建立日期',auto_now_add=True)
    datetime_edit = models.DateTimeField('修改日期',auto_now=True)

    def order_no(self):
        return str(self.id).zfill(8)

    def generate_trade_no(self):
        return self.order_no() + datetime.now().strftime("%y%m%d%H%M%S")

    def get_item_title(self):
        return ''

    def has_succeed(self):
        if self.payment_set.filter(is_success=True):
            return True
        return False
    has_succeed.admin_order_field = 'datetime_create'
    has_succeed.boolean = True
    has_succeed.short_description = '已付款?'

    def get_deserialized_cart(self):
        deserialized_cart = serializers.deserialize("json", self.serialized_cart)
        cartitem_list = []
        for cartitem in deserialized_cart:
            cartitem_list.append(cartitem.object)

        return cartitem_list

@receiver(post_save, sender=Order)
def deduct_product_stock(sender, instance, created, **kwargs):
    if created:
        deserialized_cart = instance.get_deserialized_cart()
        for cart_item in deserialized_cart:
            the_product = cart_item.product
            the_product.stock = F('stock') - cart_item.quantity
            the_product.save()

@receiver(pre_delete, sender=Order)
def return_product_stock(sender, instance, **kwargs):
    deserialized_cart = instance.get_deserialized_cart()
    for cart_item in deserialized_cart:
        the_product = cart_item.product
        the_product.stock = F('stock') + cart_item.quantity
        the_product.save()

class Payment(models.Model):

    class PaymentTypes(models.TextChoices):
        CREDIT = 'Credit', _('信用卡及 GooglePay')
        GOOGLEPAY = 'GooglePay', _('GooglePay') # (若為PC版時不支援)
        WEBATM = 'WebATM', _('網路 ATM') # (若為手機版時不支援)
        ATM = 'ATM', _('自動櫃員機')
        CVS = 'CVS', _('超商代碼')
        BARCODE = 'BARCODE', _('超商條碼') # (若為手機版時不支援)
        ALL = 'ALL', _('不指定付款方式，由綠界顯示付款方式選擇頁面。')

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    trade_no = models.CharField('廠商交易編號',max_length=20)
    type = models.CharField(
        max_length=9,
        choices=PaymentTypes.choices,
        default=PaymentTypes.CREDIT,
    )
    is_success = models.BooleanField('交易是否成功',default=False)
    datetime_create = models.DateTimeField('建立日期',auto_now_add=True)
    datetime_edit = models.DateTimeField('修改日期',auto_now=True)

    class Meta:
        get_latest_by = "datetime_create"