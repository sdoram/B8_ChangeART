from rest_framework import serializers
from .models import Article, Comment


class ArticleCreateSerializer(serializers.ModelSerializer):
    """게시글 작성, 수정 시리얼라이저"""

    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Article
        fields = "__all__"


class ArticleDetailSerializer(serializers.ModelSerializer):
    """게시글 상세보기 시리얼라이저(좋아요, 댓글까지)"""

    user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField
    # comment = 코멘트시리얼라이저 역참조

    def get_user(self, obj):
        return obj.user.nickname

    def get_user_id(self, obj):
        return obj.user.user_id

    def get_like_count(self, obj):
        return obj.like.count()

    class Meta:
        model = Article
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """댓글 시리얼라이저"""

    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("content", "nickname", "created_at", "updated_at")

    def get_nickname(self, obj):
        return obj.user.nickname
