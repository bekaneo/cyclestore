from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsAuthorOrAdmin
from .models import LikedProduct, CommentProduct, FavoriteProduct
from accounts.serializers import UserProfileSerializer
from .serializers import LikedProductSerializer, CommentProductSerializer, FavoriteProductSerializer

User = get_user_model()


class LikedProductViewSet(ModelViewSet):
    queryset = LikedProduct.objects.all()
    serializer_class = LikedProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentProductViewSet(ModelViewSet):
    queryset = CommentProduct.objects.all()
    serializer_class = CommentProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        if self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthorOrAdmin]
        return super().get_permissions()


class FavoriteProductViewSet(ModelViewSet):
    queryset = FavoriteProduct.objects.all()
    serializer_class = FavoriteProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = User.objects.get(email=request.user)
        serializer = UserProfileSerializer(queryset, context={'request': request})
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
