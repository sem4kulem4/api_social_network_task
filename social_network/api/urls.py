from django.urls import include, path

from rest_framework import routers

from .views import ArticleViewSet, FavoritesViewSet, RatingViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='articles')
router.register(r'ratings', RatingViewSet, basename='ratings')
router.register(r'favorites', FavoritesViewSet, basename='favorites')

urlpatterns = [
    path('v1/', include(router.urls)),
]
