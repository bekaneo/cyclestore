from django.contrib import admin

from products.models import Product, ProductImage


class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    max_num = 10
    min_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductImageInLine, ]
    list_display = ['user', 'name', 'category', 'price', 'description', 'brand']


# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     model = ProductImage
#     list_display = ['image', 'product']
