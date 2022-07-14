from categories.models import Type, Brand, Size
from django.contrib import admin

<<<<<<< HEAD
from categories.models import Category, Brand, Size
=======
>>>>>>> d8522092d29ccbbbfc2d0f0759fd6d5bd16442c6

@admin.register(Type)
class CategoryAdmin(admin.ModelAdmin):
    model = Type
    list_display = ['name', 'slug']


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    model = Size
    list_display = ['size_in_cm', 'size_in_inch']


@admin.register(Brand)
class SubCategoryAdmin(admin.ModelAdmin):
    model = Brand
    list_display = ['brand', 'slug']

