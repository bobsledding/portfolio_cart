from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
# Create your models here.
"""
在order必須保存的資訊
時間
付款狀態
商品、價格

"""

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_create = models.DateTimeField('建立日期',auto_now_add=True)
    datetime_edit = models.DateTimeField('修改日期',auto_now=True)
    serialized_cart = models.TextField('序列化的購物車')
    total_amount = models.PositiveIntegerField('總價')
    product_title = models.TextField('商品名以#分隔')

    def order_no(self):
        return str(self.id).zfill(8)

    def generate_trade_no(self):
        return self.order_no() + datetime.now().strftime("%y%m%d%H%M%S")

    def get_item_title(self):
        return ''

class Payment(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    trade_no = models.CharField('廠商交易編號',max_length=20)
    is_success = models.BooleanField('交易是否成功',default=False)
    datetime_create = models.DateTimeField('建立日期',auto_now_add=True)
    datetime_edit = models.DateTimeField('修改日期',auto_now=True)
    check_mac_value = models.TextField('檢查碼',max_length=20,default='')

    class Meta:
        get_latest_by = "datetime_create"