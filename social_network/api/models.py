from transliterate import translit

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum


User = get_user_model()


class Article(models.Model):
    """Модель записи."""
    title = models.CharField(max_length=100, unique=True)
    #title_transliterate = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article')
    summary = models.CharField(max_length=250)
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    view_count = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author} - {self.title}'


# class Favorite(models.Model):
#     """Модель с избранными записями."""
#     user = models.ManyToManyField(User)
#     favorite = models.ManyToManyField(Article)
#
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['user', 'favorite'],
#                 name='unique_favourite'
#             )
#         ]
#
#

class Score(models.Model):
    """Модель с оценками записей."""
    SCORE_CHOICES = (
        (-1, '-1'),
        (0, '0'),
        (1, '1'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, choices=SCORE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'article'],
                name='unique_score'
            )
        ]

    def __str__(self):
        return f'{self.score} - {self.user} - {self.article.title}'
