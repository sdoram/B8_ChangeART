from rest_framework import serializers
from .models import Article, Comment, Images, Change


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
        fields = (
            "content",
            "nickname",
            "created_at",
            "updated_at",
            "user_id",
            "article_id",
            "id",
        )

    def get_nickname(self, obj):
        return obj.user.nickname


class ArticleDetailSerializer(serializers.ModelSerializer):
    """게시글 상세보기 시리얼라이저(좋아요, 댓글까지)"""

    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comments = CommentSerializer(source="comment_set", many=True)
    images = ImageSerializer(source="images_set", many=True, read_only=True)

    def get_user(self, obj):
        return obj.user.nickname

    def get_user_id(self, obj):
        return obj.user.id

    def get_like_count(self, obj):
        return obj.like.count()

    class Meta:
        model = Article
        fields = "__all__"


class ChangeSerializer(serializers.ModelSerializer):
    """이미지 변환 시리얼라이저"""

    class Meta:
        model = Change
        fields = (
            "before_image",
            "after_image",
        )


class HomeSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    like = serializers.StringRelatedField(many=True)
    like_count = serializers.SerializerMethodField()
    comments = CommentSerializer(source="comment_set", many=True)
    comments_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    def get_user_id(self, obj):
        return obj.user.id

    def get_like_count(self, obj):
        return obj.like.count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    def get_image(self, obj):
        if obj.images_set.exists():
            first_image = obj.images_set.first()
            return {
                "id": first_image.id,
                "image": first_image.image.url,
                "article": obj.id,
            }
        else:
            return None

    class Meta:
        model = Article
        fields = "__all__"


class HomeListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    def get_like_count(self, obj):
        return obj.like.count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    def get_image(self, obj):
        if obj.images_set.exists():
            first_image = obj.images_set.first()
            return {
                "id": first_image.id,
                "image": first_image.image.url,
                "article": obj.id,
            }
        else:
            return None

    class Meta:
        model = Article
        fields = (
            "pk",
            "title",
            "image",
            "created_at",
            "user",
            "like_count",
            "comments_count",
        )
