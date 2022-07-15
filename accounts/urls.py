from django.urls import path
from .views import (RegistrationView, ActivationView, LoginView, UpdateTokenView,
                    LogoutView, RestorePasswordView, RestorePasswordCompleteView,
                    ChangePasswordView)
from .views import UserProductView
# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('products', UserProductView)


urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('activation/<str:activation_code>', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', UpdateTokenView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('restore_password/', RestorePasswordView.as_view()),
    path('restore_complete/', RestorePasswordCompleteView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('products/', UserProductView.as_view()),
]
