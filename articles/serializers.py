from rest_framework import serializers
from .models import Article, Comment, Images, Change
from users.serializers import UserProfileImageSerializer


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
    """댓글 작성, 수정, 삭제시리얼라이저"""

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


class CommentDetailSerializer(serializers.ModelSerializer):
    """게시글 상세보기에서 댓글 get용 시리얼라이저"""

    profile_image = UserProfileImageSerializer(source="user", read_only=True)
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
            "profile_image",
        )

    def get_nickname(self, obj):
        return obj.user.nickname


class ArticleDetailSerializer(serializers.ModelSerializer):
    """게시글 상세보기 시리얼라이저(좋아요, 댓글까지)"""

    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comments = CommentDetailSerializer(source="comment_set", many=True)
    images = ImageSerializer(source="images_set", many=True, read_only=True)
    profile_image = UserProfileImageSerializer(source="user", read_only=True)

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

class ImageChangeSerializer(serializers.ModelSerializer):
    """이미지 저장 시에 사용하는 시리얼라이저
    수정 가능성 높음"""

    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname
    class Meta:
        model = Change
        fields = '__all__'


class HomeSerializer(serializers.ModelSerializer):
    # 시리얼라이저로 필요한 필드
    # 좋아요 개수 카운팅
    like_count = serializers.SerializerMethodField()
    # 댓글 개수 카운팅
    comments_count = serializers.SerializerMethodField()
    # 이미지 개수 1개만 미리보기
    image = serializers.SerializerMethodField()

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
