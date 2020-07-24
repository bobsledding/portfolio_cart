from django.db import models
from django.dispatch import receiver
import os
import boto3
from django.conf import settings

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

    def __str__(self):
        return '%s-%s-$%s-庫存:%s' % (self.cat, self.title, self.price, self.stock)

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.ImageField('檔案',upload_to='product_images')
    priority = models.PositiveSmallIntegerField('排序',default=0)
    description = models.CharField('照片簡述',max_length=200,default='',blank=True,null=True)

    class Meta:
        ordering = ['priority']

def s3_delete(id):
    session = boto3.Session(
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY,
        region_name="us-east-2"
    )
    s3 = session.resource("s3")
    path_to_file = settings.PUBLIC_MEDIA_LOCATION + "/" + id
    obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, path_to_file)
    obj.delete()

@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.

    P.S.加上S3 delete
    """
    if instance.file:
        if settings.USE_S3:
            s3_delete(instance.file.name)
        else:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)

@receiver(models.signals.pre_save, sender=Image)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.

    P.S.加上S3 delete
    """
    # disable the handler during fixture loading
    if kwargs['raw']:
        return
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).file
    except sender.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if settings.USE_S3:
            s3_delete(old_file.name)
        else:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)