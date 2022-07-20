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
from reviews.models import LikedProduct, FavoriteProduct, CommentProduct
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
        serializer = ProductRetrieveSerializer(product, context={'request': request})
        return Response(serializer.data)

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
            product_id = str(request.get_full_path()).split('/')[2]
            print(product_id)
            try:
                like = LikedProduct.objects.filter(product_id=product, user=user)
                if len(like):
                    like.delete()
                    message = 'like removed'
                else:
                    LikedProduct.objects.create(product_id=product_id, user_id=user)
                    message = 'liked'
            except IndexError:
                LikedProduct.objects.create(product_id=product_id, user_id=user)
                message = 'Like'
            return Response(message, status=200)
        else:
            return Response('Requires authentication', status=status.HTTP_403_FORBIDDEN)

    @action(['GET'], detail=True)
    def favorite(self, request, pk=None):
        if request.user.is_authenticated:
            user = request.user
            product_id = str(request.get_full_path()).split('/')[2]
            print(product_id)
            try:
                like = FavoriteProduct.objects.filter(product_id=product_id, user=user)
                if len(like):
                    like.delete()
                    message = 'deleted from favorite'
                else:
                    FavoriteProduct.objects.create(product_id=product_id, user_id=user)

                    message = 'added to favorite'
            except IndexError:
                FavoriteProduct.objects.create(product_id=product_id, user_id=user)
                message = 'Like'
            return Response(message, status=200)
        else:
            return Response('Requires authentication', status=status.HTTP_403_FORBIDDEN)

    @action(['POST'], detail=True)
    def comment(self, request, pk=None):
        if request.user.is_authenticated:
            user = request.user
            product_id = str(request.get_full_path()).split('/')[2]
            text = request.data['text']
            try:
                CommentProduct.objects.create(user_id=user, product_id=product_id, text=text)
                return Response(status=status.HTTP_201_CREATED)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)

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
