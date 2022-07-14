import datetime

from rest_framework import serializers

from .models import Product, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        serializer = ProductImageSerializer(instance.images.all(),
                                            many=True, context=self.context)
        representation['images'] = serializer.data
        return representation

    def create(self, validated_data):
        validated_data['created_at'] = datetime.datetime.today()
        return super().create(validated_data)

    def save(self, **kwargs):
        self.validated_data['user'] = self.context['request'].user
        # print(self.validated_data)
        return super().save(**kwargs)


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'user']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

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
