from rest_framework import serializers
from .models import Article, Comment, Images


class ImageSerializer(serializers.ModelSerializer):
    """이미지 시리얼라이저"""

    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Images
        fields = "__all__"


class ArticleCreateSerializer(serializers.ModelSerializer):
    """게시글 작성, 수정 시리얼라이저"""

    user = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, read_only=True)

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Article
        exclude = ["like"]

    def create(self, validated_data):
        images_data = self.context.get("request").FILES
        article = Article.objects.create(**validated_data)
        for image_data in images_data.getlist("image"):
            Images.objects.create(article=article, image=image_data)
        return article

    def update(self, article, validated_data):
        article.title = validated_data.get("title", article.title)
        article.content = validated_data.get("content", article.content)

        images_data = self.context.get("request").FILES

        for image_data in images_data.getlist("image"):
            Images.objects.create(article=article, image=image_data)

        article.save()
        return article


class CommentSerializer(serializers.ModelSerializer):
    """댓글 시리얼라이저"""

    nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("content", "nickname", "created_at", "updated_at")

    def get_nickname(self, obj):
        return obj.user.nickname


class ArticleDetailSerializer(serializers.ModelSerializer):
    """게시글 상세보기 시리얼라이저(좋아요, 댓글까지)"""

    user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comments = CommentSerializer(source="comment_set", many=True)
    images = ImageSerializer(source="images_set", many=True, read_only=True)

    def get_user(self, obj):
        return obj.user.nickname

    def get_user_id(self, obj):
        return obj.user.user_id

    def get_like_count(self, obj):
        return obj.like.count()

    class Meta:
        model = Article
        fields = "__all__"
