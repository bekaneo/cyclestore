from products.models import Product
from products.serializers import ProductListSerializer, ProductSerializer
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        if self.action in ['destroy', 'update', 'create', 'partial_update']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

