from .views import CommentProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('comment', CommentProductViewSet)
urlpatterns = []

urlpatterns += router.urls
