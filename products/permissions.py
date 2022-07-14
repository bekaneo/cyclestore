from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAdminUser


#
# class IsAuthor(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         print(obj.user, 'sadsadadasdsasd')
#         return request.user.is_authenticated and request.user == obj.user


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user == obj.user)
