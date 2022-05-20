from transliterate import translit

from django.db.models import Sum

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Article, Score


class ArticleSerializer(serializers.ModelSerializer):
    #rating = serializers.SerializerMethodField()
    #title_transliterate = serializers.SerializerMethodField()
    author = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Article
        fields = '__all__'
    #
    # def get_title_transliterate(self, obj):
    #     title_transliterate = translit(obj.title, language_code='ru', reversed=True)
    #     title_transliterate = title_transliterate.strip()
    #     title_transliterate = title_transliterate.replace(' ', '-')
    #     print(title_transliterate)
    #     return title_transliterate
    #
    # def get_rating(self, obj):
    #     rating = Score.objects.filter(article_id=obj.id).aggregate(Sum('score'))
    #     return rating['score__sum']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Score
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Score.objects.all(),
                fields=('article', 'user')
            )
        ]
