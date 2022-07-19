from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import LikedProduct, CommentProduct, FavoriteProduct
from .serializers import LikedProductSerializer, CommentProductSerializer, FavoriteProductSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import permissions
from .permissions import IsAuthorOrAdmin


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
