from django.shortcuts import render

from rest_framework import viewsets, mixins

from .models import Article, Score
from .permissions import AuthorArticleOrReadOnly, AuthorScoreOrReadOnly
from .serializers import ArticleSerializer, RatingSerializer



class ArticleViewSet(viewsets.ModelViewSet):
    AVAILABLE_SCORES = (-1, 0, 1)
    # pagination_class = None
    # permission_classes = None
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (AuthorArticleOrReadOnly,)
    #lookup_field = 'title_transliterate'

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.view_count = obj.view_count + 1
        obj.save(update_fields=("view_count",))
        # print(obj.id)
        # print(request.user)
        # print(request.user.id)
        # print(request.data['rating'])
        # if 'rating' in request.data and request.data['rating'] in self.AVAILABLE_SCORES:
        #     if Score.objects.filter(user=request.user, article=obj, score=request.data['rating']):
        #         raise Exception('незя')
        #     Score.objects.get(user=request.user, article=obj.id,).delete()
        #     Score.objects.create(user=request.user, article=obj, score=request.data['rating'])
        #     obj.save()

        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (AuthorScoreOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
