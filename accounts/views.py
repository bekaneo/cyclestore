from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .permissions import IsUserOrAdmin
from products.serializers import ProductSerializer
from .serializers import *
from products.models import Product

User = get_user_model()


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer)
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.create()
            return Response('Successfully created', status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Account is activated')
        except User.DoesNotExist:
            raise Http404


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class UpdateTokenView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get('refresh_token')
        if token is not None:
            token_object = RefreshToken(token)
            token_object.blacklist()
            return Response('Logout successfully')
        else:
            return Response('There is no token', status=400)


class RestorePasswordView(APIView):
    @swagger_auto_schema(request_body=RestorePasswordSerializer)
    def post(self, request):
        print(request.data)
        data = request.data
        serializer = RestorePasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_code()
            return Response('Check your email for code')


class RestorePasswordCompleteView(APIView):
    @swagger_auto_schema(request_body=RestorePasswordCompleteSerializer)
    def post(self, request):
        data = request.data
        serializer = RestorePasswordCompleteSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Password is successfully updated')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Password is successfully updated')


# class UserProductView(ListAPIView):
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         email = self.request.user
#         return Product.objects.filter(user_id=email)
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = ProductSerializer(queryset, many=True)
#         return Response(serializer.data)


class UserProfileView(ListAPIView, UpdateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    # permission_classes = []
    #
    # def get_object(self, username):
    #     return User.objects.filter(name=username)
    #
    # def get_queryset(self,):
    #     return User.objects.filter(name=username)

    def get_permissions(self):
        if self.request.method in ['GET']:
            self.permission_classes = [IsAuthenticated]
        if self.request.method in ['PATCH', 'PUT']:
            self.permission_classes = [IsUserOrAdmin]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        queryset = User.objects.get(email=request.user)
        serializer = UserProfileSerializer(queryset, context={'request': request})
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, *args, **kwargs):
        instance = User.objects.get(email=request.user)
        serializer = UserProfileUpdateSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(ListAPIView):
    serializer_class = UserProfileSerializer

    def list(self, request, username, *args, **kwargs):
        queryset = User.objects.get(name=username)
        serializer = ProfileSerializer(queryset, context={'request': request})
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)

    # def patch(self, request, username, *args, **kwargs):
    #     instance = User.objects.get(name=username)
    #     # print(type(instance.email))
    #     # print(type())
    #     if instance.email == str(request.user) or request.user.is_staff:
    #         data = request.data
    #         serializer = UserProfileUpdateSerializer(instance, data=data)
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save()
    #             return Response(serializer.data)
    #     else:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
# def update(self, request, username, *args, **kwargs):
#     instance = self.get_object(username)
#     serializer = self.get_serializer(instance, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response('good')
#     return Response('bad')


# class UserProfileViewSet(ModelViewSet):
#     serializer_class = UserProfileSerializer
#
#     permission_classes = [AllowAny]
#
#     def get_queryset(self, username):
#         return User.objects.filter(name=username)
#
#     def get_permissions(self):
#         if self.action in ['list', 'retrieve']:
#             self.permission_classes = [permissions.AllowAny]
#         if self.action in ['update', 'partial_update']:
#             self.permission_classes = [IsAuthorOrAdmin]
#         return super().get_permissions()
