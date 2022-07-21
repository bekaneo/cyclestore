from rest_framework import serializers
from .models import LikedProduct, CommentProduct, FavoriteProduct
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

User = get_user_model()


class LikedProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = LikedProduct
        fields = '__all__'

    def validate(self, attrs):
        attrs['user'] = self.context.get('request').user
        return super().validate(attrs)

    # def create(self, validated_data):
    #     user = validated_data['user']
    #     product = validated_data['product']
    #     if LikedProduct.objects.filter(user=user, product=product):
    #         LikedProduct.objects.filter(user=user, product=product).delete()
    #         validated_data = {}
    #         return super().create(validated_data)
    #     else:
    #         return super().create(validated_data)

    # def save(self, **kwargs):
    #     try:
    #         super().save(**kwargs)
    #     except IntegrityError:
    #         print('')


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

    def create(self, validated_data):
        user = validated_data['user']
        product = validated_data['product']
        if FavoriteProduct.objects.filter(user=user, product=product):
            FavoriteProduct.objects.filter(user=user, product=product).delete()
            validated_data = {}
            return super().create(validated_data)
        else:
            return super().create(validated_data)

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except IntegrityError:
            print('')
