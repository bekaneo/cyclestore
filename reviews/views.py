from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import LikedProduct
from .serializers import LikedProductSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class LikedProductViewSet(ModelViewSet):
    queryset = LikedProduct.objects.all()
    serializer_class = LikedProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
