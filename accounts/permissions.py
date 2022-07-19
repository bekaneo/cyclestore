from rest_framework.permissions import BasePermission, IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()


class IsUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff

    # def has_permission(self, request, view):
    #     name = str(request.get_full_path()).split('/')[-1]
    #     email = User.objects.get(name=name).email
    #     return str(request.user) == str(email) or request.user.is_staff
