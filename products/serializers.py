import datetime

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Product, ProductImage

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    # name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        serializer = ProductImageSerializer(instance.images.all(),
                                            many=True, context=self.context)
        representation['images'] = serializer.data
        representation['username'] = User.objects.get(email=representation['user']).name
        return representation

    def save(self, **kwargs):
        email = self.context['request'].user
        name = User.objects.get(email=email).name
        self.validated_data['user'] = email
        # self.validated_data['name'] = name
        self.validated_data['created_at'] = datetime.datetime.today()
        return super().save(**kwargs)

    def create(self, validated_data):
        images_data = self.context.get('view').request.FILES
        product = Product.objects.create(**validated_data)
        for image in images_data.values():
            ProductImage.objects.create(product=product, image=image)
        return product


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
