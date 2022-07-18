from .views import LikedProductVieSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('like', LikedProductVieSet)

urlpatterns = []

urlpatterns += router.urls
