from django.contrib import admin
from .models import Order, Payment
# Register your models here.

class PaymentInline(admin.StackedInline):
    model = Payment
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [PaymentInline]
    list_display = ('user', 'has_succeed', 'product_title', 'datetime_create')

admin.site.register(Order, OrderAdmin)
