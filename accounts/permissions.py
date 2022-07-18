from rest_framework.permissions import BasePermission, IsAuthenticated


class IsUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj)
        return request.user == obj.email or request.user.is_staff

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
