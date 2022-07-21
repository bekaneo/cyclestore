from rest_framework import serializers
from .models import LikedProduct, CommentProduct, FavoriteProduct
from django.contrib.auth import get_user_model

User = get_user_model()


class LikedProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = LikedProduct
        fields = '__all__'

    def validate(self, attrs):
        attrs['user'] = self.context.get('request').user
        return super().validate(attrs)


class CommentProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = CommentProduct
        fields = '__all__'

    def validate(self, attrs):
        attrs['user'] = self.context.get('request').user
        return super().validate(attrs)


class FavoriteProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = FavoriteProduct
        fields = '__all__'

    def validate(self, attrs):
        attrs['user'] = self.context.get('request').user
        return super().validate(attrs)

