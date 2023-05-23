from django.db import models
from users.models import User


# 게시글 모델
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    content = models.TextField(null=True)
    before_image = models.ImageField(
        blank=True, null=True, upload_to="original_images/"
    )
    after_image = models.ImageField(
        blank=True, null=True, upload_to="transfer_images/"
    )  # null=True 추후 삭제예정
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name="like_article", blank=True)

    def __str__(self):
        return str(self.title)
