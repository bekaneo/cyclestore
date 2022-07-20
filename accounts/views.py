from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .permissions import IsUserOrAdmin
from .serializers import *

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


class UserProfileView(ListAPIView, UpdateAPIView):
    serializer_class = UserProfileSerializer

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

    @swagger_auto_schema(request_body=UserProfileUpdateSerializer)
    def patch(self, request, *args, **kwargs):
        instance = User.objects.get(email=request.user)
        serializer = UserProfileUpdateSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(ListAPIView):
    serializer_class = UserProfileSerializer

    def list(self, request, username, *args, **kwargs):
        queryset = User.objects.get(name=username)
        serializer = ProfileSerializer(queryset, context={'request': request})
        if serializer.data:
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
