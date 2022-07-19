from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAdminUser
from products.models import Product


#
# class IsAuthor(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         print(obj.user, 'sadsadadasdsasd')
#         return request.user.is_authenticated and request.user == obj.user


class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff


class IsImageAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = Product.objects.get(id=obj.product_id).user
        return request.user == user or request.user.is_staff
