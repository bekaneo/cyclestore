from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import LikedProduct
from .serializers import LikedProductSerializer


class LikedProductVieSet(ModelViewSet):
    queryset = LikedProduct.objects.all()
    serializer_class = LikedProductSerializer
