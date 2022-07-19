from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter
from .views import (RegistrationView, ActivationView, LoginView, UpdateTokenView,
                    LogoutView, RestorePasswordView, RestorePasswordCompleteView,
                    ChangePasswordView, ProfileView)
from .views import UserProfileView

# router = DefaultRouter()
# router.register('profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('activation/<str:activation_code>', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', UpdateTokenView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('restore_password/', RestorePasswordView.as_view()),
    path('restore_complete/', RestorePasswordCompleteView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    # path('/', UserProductView.as_view()),
    path('profile/', UserProfileView.as_view()),
    path('profile/<str:username>', ProfileView.as_view())
]
# urlpatterns += router.urls
