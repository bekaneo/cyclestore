from products.views import ProductViewSet, ProductImagesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('images', ProductImagesViewSet)

urlpatterns = []

urlpatterns += router.urls


