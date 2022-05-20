from transliterate import translit

from django.db.models import Sum

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Article, Score


class ArticleSerializer(serializers.ModelSerializer):
    #rating = serializers.SerializerMethodField()
    title_transliterate = serializers.CharField(read_only=True)
    author = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = '__all__'

    # def get_rating(self, obj):
    #     rating = Score.objects.filter(article_id=obj.id).aggregate(Sum('score'))
    #     return rating['score__sum']


class RatingSerializer(serializers.ModelSerializer):
    SCORE_CHOICES = (
        (-1, '-1'),
        (0, '0'),
        (1, '1'),
    )
    user = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    score = serializers.ChoiceField(choices=SCORE_CHOICES)

    class Meta:
        model = Score
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Score.objects.all(),
                fields=('article', 'user')
            )
        ]
