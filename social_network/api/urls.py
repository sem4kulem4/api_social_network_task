from django.urls import include, path

from rest_framework import routers
from rest_framework.authtoken import views

from .views import ArticleViewSet, RatingViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='articles')
router.register(r'ratings', RatingViewSet, basename='ratings')

urlpatterns = [
    path('v1/', include(router.urls)),
]
