from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='Cart_product')
    def get_total(self):
        total = 0
        for cart_product in self.cart_product_set.all():
            total += cart_product.temp_price * cart_product.quantity
        return total

    def get_product_total(self):
        total = 0
        for cart_product in self.cart_product_set.all():
            total += cart_product.product.price * cart_product.quantity
        return total

    def has_invalid(self):
        for cart_product in self.cart_product_set.all():
            if not cart_product.is_buyable():
                return True
        return False

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

class Cart_product(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    temp_title = models.CharField('暫存商品名',max_length=200)
    temp_price = models.PositiveIntegerField('暫存價格',default=99999)
    quantity = models.PositiveSmallIntegerField('數量',default=0)

    # test needed
    def is_buyable(self):
        if self.temp_price != self.product.price:
            return False
        if self.quantity > self.product.stock:
            return False
        return True

    def get_subtotal(self):
        return self.quantity * self.temp_price

    def get_product_subtotal(self):
        return self.quantity * self.product.price