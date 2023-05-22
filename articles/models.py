from django.db import models


class Comment(models.Model):
    article_id = models.ForeignKey(
        Article, verbose_name="게시글", on_delete=models.CASCADE
    )
    user_id = models.models.ForeignKey(
        User, verbose_name="작성자", on_delete=models.CASCADE
    )
    content = models.CharField("내용", max_length=300)
    created_at = models.DateTimeField("작성날짜", auto_now_add=True)
    updated_at = models.DateTimeField("수정날짜", auto_now=True)
