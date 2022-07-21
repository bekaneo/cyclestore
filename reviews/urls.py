from .views import CommentProductViewSet, FavoriteProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('comment', CommentProductViewSet)
router.register('favorite', FavoriteProductViewSet)
urlpatterns = []

urlpatterns += router.urls
