from rest_framework.routers import DefaultRouter

from products.views import ProductViewSet, ProductImagesViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('images', ProductImagesViewSet)
urlpatterns = []

urlpatterns += router.urls
