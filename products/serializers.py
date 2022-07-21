from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Product, ProductImage
from reviews.models import LikedProduct, FavoriteProduct
from reviews.serializers import LikedProductSerializer, CommentProductSerializer, FavoriteProductSerializer

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        likes = LikedProductSerializer(instance.like.all(), many=True, context={'request': request}).data
        serializer = ProductImageSerializer(instance.images.all(),
                                            many=True, context={'request': request})
        comment = CommentProductSerializer(instance.comment.all(), many=True, context={'request': request})

        representation['username'] = User.objects.get(email=representation['user']).name
        representation['is_author'] = str(self.context.get('request').user) == str(representation['user'])
        representation['is_liked'] = self.check_like(instance, request, representation['id'])
        representation['is_favorite'] = self.check_favorite(instance, request, representation['id'])
        representation['images'] = serializer.data
        representation['like'] = len(likes)
        representation['comments'] = len(comment.data)

        return representation

    def save(self, **kwargs):
        email = self.context.get('request').user
        self.validated_data['user'] = email
        return super().save(**kwargs)

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        product = Product.objects.create(**validated_data)
        for image in images_data._getlist('image'):
            ProductImage.objects.create(product=product, image=image)
        return product

    def check_like(self, instance, request, product_id):
        try:
            LikedProductSerializer(instance.like.get(user=request.user, product=product_id),
                                   context={'request': request})
            return True
        except LikedProduct.DoesNotExist:
            return False

    def check_favorite(self, instance, request, product_id):
        try:
            FavoriteProductSerializer(instance.favorite.get(user=request.user, product=product_id),
                                      context={'request': request})
            return True
        except FavoriteProduct.DoesNotExist:
            return False


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        likes = LikedProductSerializer(instance.like.all(), many=True, context={'request': request}).data
        recommendations = Product.objects.filter(category=representation['category'])[:5]
        recommendations = ProductSerializer(recommendations, many=True, context={'request': request})
        comments = CommentProductSerializer(instance.comment.all(), many=True, context={'request': request})
        images = ProductImageSerializer(instance.images.all(),
                                        many=True, context={'request': request})

        representation['username'] = User.objects.get(email=representation['user']).name
        representation['is_author'] = str(self.context.get('request').user) == str(representation['user'])
        representation['is_liked'] = self.check_like(instance, request, representation['id'])
        representation['is_favorite'] = self.check_favorite(instance, request, representation['id'])
        representation['like'] = len(likes)
        representation['images'] = images.data
        representation['comments'] = comments.data
        representation['recommendation'] = recommendations.data

        return representation

    def check_like(self, instance, request, product_id):
        try:
            LikedProductSerializer(instance.like.get(user=request.user, product=product_id),
                                   context={'request': request})
            return True
        except LikedProduct.DoesNotExist:
            return False

    def check_favorite(self, instance, request, product_id):
        try:
            FavoriteProductSerializer(instance.favorite.get(user=request.user, product=product_id),
                                      context={'request': request})
            return True
        except FavoriteProduct.DoesNotExist:
            return False


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'product_id')

    def get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self.get_image_url(instance)
        return representation

    def create(self, validated_data):
        return ProductImage.objects.create(product_id=self.context.get('product'), **validated_data)
