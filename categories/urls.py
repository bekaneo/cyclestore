from rest_framework.routers import DefaultRouter
from .views import TypeViewSet, BrandViewSet, SizeViewSet

router = DefaultRouter()
router.register('type', TypeViewSet,)
router.register('brand', BrandViewSet)
router.register('size', SizeViewSet)

urlpatterns = []

urlpatterns += router.urls
