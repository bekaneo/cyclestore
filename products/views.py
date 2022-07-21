from products.models import Product, ProductImage
from products.serializers import ProductRetrieveSerializer, ProductSerializer, ProductImageSerializer
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .filters import ProductPriceFilter
from rest_framework.decorators import action
from reviews.models import LikedProduct, FavoriteProduct, CommentProduct
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from reviews.serializers import CommentProductSerializer
from .tasks import send_notification
from django.core.mail import send_mail
from cycle import settings

from .permissions import IsAuthorOrAdmin, IsImageAuthorOrAdmin


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['title', 'description']
    filterset_class = ProductPriceFilter
    permission_classes = [permissions.AllowAny]

    # def get_queryset(self):
    #     user = self.request.user
    #     return Product.objects.exclude(user=user).order_by('id')
    @swagger_auto_schema(request_body=ProductSerializer)
    def create(self, request, *args, **kwargs):
        product_serializer = ProductSerializer(data=request.POST, context={'request': request})
        if product_serializer.is_valid(raise_exception=True):
            product = product_serializer.save()
            product_data = product_serializer.data

        images = []
        for image in request.FILES.getlist('image'):
            data = {'image': image}
            image_serializer = ProductImageSerializer(data=data, context={'product': product.id, 'request': request})
            if image_serializer.is_valid(raise_exception=True):
                image_serializer.save()
                images.append(image_serializer.data)

        data = {'product_data': product_data, 'image': images}
        return Response(data, status=status.HTTP_201_CREATED)

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
            user = request.user
            product_id = str(request.get_full_path()).split('/')[2]
            try:
                like = LikedProduct.objects.get(product_id=product_id, user=user)
                like.delete()
                return Response('like removed', status=status.HTTP_200_OK)
            except LikedProduct.DoesNotExist:
                LikedProduct.objects.create(product_id=product_id, user=user)
                return Response('liked', status=status.HTTP_201_CREATED)
        else:
            return Response('Requires authentication', status=status.HTTP_403_FORBIDDEN)

    @action(['GET'], detail=True)
    def favorite(self, request, pk=None):
        if request.user.is_authenticated:
            user = request.user
            product_id = str(request.get_full_path()).split('/')[2]
            try:
                fav = FavoriteProduct.objects.get(product_id=product_id, user=user)
                fav.delete()
                return Response('removed from favorites', status=status.HTTP_200_OK)
            except FavoriteProduct.DoesNotExist:
                product = FavoriteProduct.objects.create(product_id=product_id, user=user)
                product_id = product.product_id
                user = product.user
                product_data = Product.objects.get(id=product_id)
                author = product_data.user
                title = product_data.title
                desc = product_data.description
                send_notification.delay(str(user), str(title), str(author), str(desc))
                return Response('added to favorites', status=status.HTTP_201_CREATED)
        else:
            return Response('Requires authentication', status=status.HTTP_403_FORBIDDEN)

    @swagger_auto_schema(request_body=CommentProductSerializer)
    @action(['POST'], detail=True)
    def comment(self, request, pk=None):
        if request.user.is_authenticated:
            user = request.user
            product_id = str(request.get_full_path()).split('/')[2]
            text = request.data['text']
            try:
                CommentProduct.objects.create(user_id=user, product_id=product_id, text=text)
                return Response(status=status.HTTP_201_CREATED)
            except CommentProduct.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status.HTTP_403_FORBIDDEN)

    # @action(['DELETE'], detail=True)
    # def comment(self, request, pk=None):
    #     if request.user.is_staff:
    #         user = request.user
    #         product_id = str(request.get_full_path()).split('/')[2]
    #         text = request.data['text']
    #         try:
    #             CommentProduct.objects.get(user_id=user, product_id=product_id, text=text).delete()
    #             return Response(status=status.HTTP_204_NO_CONTENT)
    #         except CommentProduct.DoesNotExist:
    #             return Response(status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response(status.HTTP_403_FORBIDDEN)


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
