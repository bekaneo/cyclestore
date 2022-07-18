from rest_framework.permissions import BasePermission, IsAuthenticated
from django.contrib.auth import get_user_model

User = get_user_model()


class IsUserOrAdmin(BasePermission):

    def has_permission(self, request, view):
        name = str(request.get_full_path()).split('/')[-1]
        email = User.objects.get(name=name).email
        print(name)
        print(request.user)
        print(email)
        return str(request.user) == str(email) or request.user.is_staff
