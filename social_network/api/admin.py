from django.contrib import admin

from .models import Article, Favorite, Score

admin.site.register(Article)
admin.site.register(Favorite)
admin.site.register(Score)
