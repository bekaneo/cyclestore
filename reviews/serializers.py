from rest_framework.serializers import ModelSerializer
from .models import LikedProduct


class LikedProductSerializer(ModelSerializer):
    class Meta:
        model = LikedProduct
        fields = '__all__'
