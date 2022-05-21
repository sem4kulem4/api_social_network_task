from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from django.db.models import Sum

from .models import Article, Favorite, Score
from .permissions import AuthorArticleOrReadOnly, AuthorScoreAndFavoriteOrReadOnly
from .serializers import ArticleSerializer, FavoriteSerializer, RatingSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    AVAILABLE_SCORES = (-1, 0, 1)
    serializer_class = ArticleSerializer
    filter_backends = (filters.OrderingFilter,)
    filterset_fields = ('pub_date', 'rating')
    permission_classes = (AuthorArticleOrReadOnly,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'title_transliterate'

    def get_queryset(self):
        if self.request.query_params.get('liked'):
            queryset = Article.objects.filter(score__user=self.request.user, score__score=1)
            return queryset
        elif self.request.query_params.get('favorite'):
            queryset = Article.objects.filter(favorite__user=self.request.user)
            return queryset
        else:
            queryset = Article.objects.all()
            return queryset

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.view_count = obj.view_count + 1
        obj.save(update_fields=("view_count",))
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (AuthorScoreAndFavoriteOrReadOnly,)

    def perform_create(self, serializer):
        if serializer.validated_data['score'] == 0:
            raise Exception('Cannot create a ZERO score')
        serializer.save(user=self.request.user)
        rating = Score.objects.filter(
            article=serializer.validated_data['article']
        ).aggregate(Sum('score')).get('score__sum')
        article = Article.objects.get(
            id=serializer.initial_data.get('article')
        )
        article.rating = rating
        article.save()

    def perform_update(self, serializer):
        rating = Score.objects.filter(
            article=serializer.validated_data['article']
        ).aggregate(Sum('score')).get('score__sum')
        article = Article.objects.get(id=serializer.initial_data.get('article'))
        if serializer.validated_data['score'] == 0:
            Score.objects.get(
                user=self.request.user,
                article_id=serializer.validated_data['article']
            ).delete()
            article.rating = rating
            article.save()
            raise Exception(f'Your score of article {article.title} has been deleted ')
        else:
            super(RatingViewSet, self).perform_update(serializer)
            article.rating = rating
            article.save()


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (AuthorScoreAndFavoriteOrReadOnly, )

    def get_queryset(self):
        queryset = Favorite.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
