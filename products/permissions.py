from rest_framework.permissions import BasePermission

from products.models import Product


class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff


class IsImageAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = Product.objects.get(id=obj.product_id).user
        return request.user == user or request.user.is_staff
