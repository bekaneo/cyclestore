from rest_framework.serializers import ModelSerializer
from .models import Type, Size, Brand


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class SizeSerializer(ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'
