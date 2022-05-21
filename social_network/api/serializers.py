from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Article, Favorite, Score


class ArticleSerializer(serializers.ModelSerializer):
    title_transliterate = serializers.CharField(read_only=True)
    author = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Article
        fields = '__all__'


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


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = '__all__'
