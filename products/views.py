from products.models import Product, ProductImage
from products.serializers import ProductRetrieveSerializer, ProductSerializer, ProductImageSerializer
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .filters import ProductPriceFilter
from rest_framework.decorators import action
from reviews.serializers import LikedProductSerializer
from reviews.models import LikedProduct, FavoriteProduct
from rest_framework.response import Response

from .permissions import IsAuthorOrAdmin, IsImageAuthorOrAdmin


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('created_at')
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'description']
    filterset_class = ProductPriceFilter
    permission_classes = [permissions.AllowAny]

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

    @action(['GET'], detail=True)
    def like(self, request, pk=None):
        if request.user.is_authenticated:
            product = self.get_object()
            user = request.user
            try:
                like = LikedProduct.objects.filter(product_id=product, user=user)
                print(len(like))
                if len(like):
                    like.delete()
                    message = 'like removed'
                else:
                    LikedProduct.objects.create(product_id=product.id, user_id=user)
                    message = 'liked'
            except IndexError:
                LikedProduct.objects.create(product_id=product.id, user_id=user)
                message = 'Like'
            return Response(message, status=200)
        else:
            return Response('Requires authentication', status=status.HTTP_403_FORBIDDEN)
        # @action(['GET'], detail=True)
        # def favorite(self, request, pk=None):
        #     product = self.get_object()
        #     user = request.user
        #     try:
        #         favorites = Favorites.objects.filter(product_id=product, author=user)
        #         res = not favorites[0].favorites
        #         if res:
        #             favorites[0].save()
        #         else:
        #             favorites.delete()
        #         message = 'In favorites' if favorites else 'Not in favorites'
        #     except IndexError:
        #         Favorites.objects.create(product_id=product.id, author=user, favorites=True)
        #         message = 'In favorites'
        #     return Response(message, status=200)


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
