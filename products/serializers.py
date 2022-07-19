import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Product, ProductImage
from reviews.serializers import LikedProductSerializer

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    # name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        # print(f'asdsadas {(instance.like.all())}')
        # likes = LikedProductSerializer(instance.like.all(), many=True).data
        representation = super().to_representation(instance)
        # print(likes)
        serializer = ProductImageSerializer(instance.images.all(),
                                            many=True, context=self.context)
        representation['images'] = serializer.data
        representation['username'] = User.objects.get(email=representation['user']).name
        # representation['like'] = likes
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
            ProductImage.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        images_data = self.context.get('view').request.FILES
        print(validated_data)
        Product.objects.update(**validated_data)
        for image in images_data.values():
            ProductImage.objects.update_or_create(product=instance, image=image)
        return super().update(instance, validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'user']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image',)

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
