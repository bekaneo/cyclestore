from products.models import Product, ProductImage
from products.serializers import ProductRetrieveSerializer, ProductSerializer, ProductImageSerializer
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .filters import ProductPriceFilter

from .permissions import IsAuthorOrAdmin, IsImageAuthorOrAdmin


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('created_at')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['title', 'description']

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        product.views += 1
        product.save()
        self.serializer_class = ProductRetrieveSerializer
        return super().retrieve(request, *args, **kwargs)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        if self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsAuthorOrAdmin]
        return super().get_permissions()


class ProductImagesViewSet(ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        if self.action in ['create']:
            self.permission_classes = [permissions.IsAuthenticated]
        if self.action in ['destroy', 'update', 'partial_update']:
            self.permission_classes = [IsImageAuthorOrAdmin]
        return super().get_permissions()
