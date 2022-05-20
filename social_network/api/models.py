from transliterate import translit

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum


User = get_user_model()


class Article(models.Model):
    """Модель записи."""
    title = models.CharField(max_length=100, unique=True)
    title_transliterate = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article')
    summary = models.CharField(max_length=250)
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    view_count = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        transliterate = translit(self.title, language_code='ru', reversed=True)
        self.title_transliterate = transliterate.strip().replace(' ', '-')
        return super(Article, self).save(*args, **kwargs)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='score')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='score')
    score = models.IntegerField(default=0, choices=SCORE_CHOICES)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'article'],
                name='unique_score'
            )
        ]

    # def save(self, *args, **kwargs):
    #     rating = Score.objects.filter(article_id=self.article).aggregate(Sum('score'))
    #     Article.objects.get(id=self.article).update(rating=rating)
    #     return super(Score, self).save()
    # я так понял тут надо что то переопределить(это не робит)

    def __str__(self):
        return f'{self.score} - {self.user} - {self.article.title}'
