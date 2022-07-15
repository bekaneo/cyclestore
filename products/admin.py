from django.contrib import admin

from products.models import Product, ProductImage


class ProductImageInLine(admin.TabularInline):
    model = ProductImage
    max_num = 10
    min_num = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInLine, ]

