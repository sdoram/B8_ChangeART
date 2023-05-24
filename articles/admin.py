from django.contrib import admin
from articles.models import Article, Images, Comment

admin.site.register(Article)
admin.site.register(Images)
admin.site.register(Comment)
