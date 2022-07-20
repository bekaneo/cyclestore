import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Product, ProductImage
from reviews.models import LikedProduct, FavoriteProduct
from reviews.serializers import LikedProductSerializer, CommentProductSerializer, FavoriteProductSerializer

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    # name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        request = self.context.get('request')
        likes = LikedProductSerializer(instance.like.all(), many=True).data
        representation = super().to_representation(instance)
        representation['is_author'] = str(self.context.get('request').user) == str(representation['user'])
        try:
            LikedProductSerializer(instance.like.get(user=request.user, product=representation['id']))
            representation['is_liked'] = True
        except:
            representation['is_liked'] = False
        try:
            FavoriteProductSerializer(instance.favorite.get(user=request.user, product=representation['id']))
            representation['is_favorite'] = True
        except:
            representation['is_favorite'] = False
        serializer = ProductImageSerializer(instance.images.all(),
                                            many=True, context=self.context)
        comment = CommentProductSerializer(instance.comment.all(), many=True)
        representation['images'] = serializer.data
        representation['username'] = User.objects.get(email=representation['user']).name
        representation['like'] = len(likes)
        representation['comments'] = len(comment.data)

        return representation

    def save(self, **kwargs):
        email = self.context['request'].user
        self.validated_data['user'] = email
        self.validated_data['created_at'] = datetime.datetime.now()
        return super().save(**kwargs)

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        product = Product.objects.create(**validated_data)
        for image in images_data.values():
            ProductImage.objects.update_or_create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        images_data = self.context.get('view').request.FILES
        Product.objects.update(**validated_data)
        for image in images_data.values():
            ProductImage.objects.update_or_create(product=instance, image=image)
        return super().update(instance, validated_data)


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        representation['username'] = User.objects.get(email=representation['user']).name
        representation['is_author'] = str(self.context.get('request').user) == str(representation['user'])
        likes = LikedProductSerializer(instance.like.all(), many=True, context={'request': request}).data
        recommendation = Product.objects.filter(category=representation['category'])[:5]
        recommendation = ProductSerializer(recommendation, many=True, context={'request': request})
        comment = CommentProductSerializer(instance.comment.all(), many=True, context={'request': request})
        serializer = ProductImageSerializer(instance.images.all(),
                                            many=True, context={'request': request})
        try:
            LikedProductSerializer(instance.like.get(user=request.user, product=representation['id']))
            representation['is_liked'] = True
        except:
            representation['is_liked'] = False
        try:
            FavoriteProductSerializer(instance.favorite.get(user=request.user, product=representation['id']))
            representation['is_favorite'] = True
        except:
            representation['is_favorite'] = False
        representation['images'] = serializer.data
        representation['comments'] = comment.data
        representation['like'] = len(likes)
        representation['recommendation'] = recommendation.data

        return representation


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
