from django.contrib import admin
from categories.models import Category, SubCategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name', 'slug']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    model = SubCategory
    list_display = ['name', 'slug', 'category']
# Register your models here.
