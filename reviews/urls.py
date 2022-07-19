from .views import LikedProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('like', LikedProductViewSet)

urlpatterns = []

urlpatterns += router.urls
