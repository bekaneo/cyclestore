from rest_framework.urlpatterns import format_suffix_patterns

from products.views import ProductViewSet, ProductImagesViewSet
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('images', ProductImagesViewSet)
# product_retrieve = ProductViewSet.as_view({'get': 'retrieve'})
urlpatterns = []
# urlpatterns = format_suffix_patterns([
#     path('products/<int:pk>/like', product_retrieve)
# ])

urlpatterns += router.urls
