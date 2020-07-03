from django.contrib import admin
from .models import Product, Image
from django.utils.html import mark_safe
# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image
    extra = 1
    readonly_fields = ["file_image"]
    def file_image(self, obj):
        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.file.url,
            width=obj.file.width,
            height=obj.file.height,)
        )

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

admin.site.register(Product, ProductAdmin)
