from django.db import models
from users.models import User


# 게시글 모델
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField()
    # null=True 추후 삭제예정
    after_image = models.ImageField(blank=True, null=True, upload_to="transfer_images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name="like_article", blank=True)

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    article = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="작성자", on_delete=models.CASCADE)
    content = models.CharField("내용", max_length=300)
    created_at = models.DateTimeField("작성날짜", auto_now_add=True)
    updated_at = models.DateTimeField("수정날짜", auto_now=True)
