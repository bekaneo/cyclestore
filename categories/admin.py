from django.contrib import admin

from categories.models import Category, Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name', 'slug']


@admin.register(Brand)
class SubCategoryAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['brand', 'slug']
