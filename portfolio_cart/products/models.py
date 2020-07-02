from django.db import models
from django.dispatch import receiver
import os

# Create your models here.
class Product(models.Model):
    title = models.CharField('商品名',max_length=200)
    cat = models.CharField('分類',max_length=200, default='未分類')
    price = models.PositiveIntegerField('價格',default=99999)
    stock = models.PositiveSmallIntegerField('庫存',default=0)
    description = models.TextField('詳細說明',default='')
    is_feature_product = models.BooleanField('是主打商品',default=False)
    datetime_create = models.DateTimeField('建立日期',auto_now_add=True)
    datetime_edit = models.DateTimeField('修改日期',auto_now=True)

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ImageField('檔案',upload_to='product_images')
    priority = models.PositiveSmallIntegerField('排序',default=0)
    description = models.CharField('照片簡述',max_length=200,default='')

@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=Image)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)