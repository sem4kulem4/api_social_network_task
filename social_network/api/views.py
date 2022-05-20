import http

from django.shortcuts import render
from requests import Response

from rest_framework import viewsets, mixins

from django.http import HttpResponseBadRequest

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
    lookup_field = 'title_transliterate'

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
    permission_classes = (AuthorScoreOrReadOnly,)

    def perform_create(self, serializer):
        print(serializer.validated_data)
        if serializer.validated_data['score'] == 0:
            raise Exception('Cannot create a ZERO score')
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.validated_data['score'] == 0:
            Score.objects.get(user=self.request.user, article_id=serializer.validated_data['article']).delete()
        return super(RatingViewSet, self).perform_update(serializer)