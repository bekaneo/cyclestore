from categories.models import Type, Brand, Size
from django.contrib import admin


@admin.register(Type)
class CategoryAdmin(admin.ModelAdmin):
    model = Type
    list_display = ['name', 'slug']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    model = Size
    list_display = ['inch']


@admin.register(Brand)
class SubCategoryAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['brand', 'slug']
