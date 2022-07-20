from .views import LikedProductViewSet, CommentProductViewSet, FavoriteProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register('like', LikedProductViewSet)
router.register('comment', CommentProductViewSet)
# router.register('favorite', FavoriteProductViewSet)
urlpatterns = []

urlpatterns += router.urls
