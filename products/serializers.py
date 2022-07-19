import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Product, ProductImage
from reviews.serializers import LikedProductSerializer, CommentProductSerializer

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    # name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        likes = LikedProductSerializer(instance.like.all(), many=True).data
        representation = super().to_representation(instance)
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
        print(images_data)
        product = Product.objects.create(**validated_data)
        for image in images_data.values():
            ProductImage.objects.update_or_create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        images_data = self.context.get('view').request.FILES
        # print(validated_data)
        Product.objects.update(**validated_data)
        # ProductImage.objects.bulk_update(product_id=instance, image=images_data)
        for image in images_data.values():
            ProductImage.objects.update_or_create(product=instance, image=image)
        return super().update(instance, validated_data)


class ProductRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['username'] = User.objects.get(email=representation['user']).name
        likes = LikedProductSerializer(instance.like.all(), many=True).data
        recommendation = Product.objects.filter(category=representation['category'])[:5]
        recommendation = ProductSerializer(recommendation, many=True)
        comment = CommentProductSerializer(instance.comment.all(), many=True)
        serializer = ProductImageSerializer(instance.images.all(),
                                            many=True, context=self.context)
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
