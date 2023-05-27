from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from .models import User, Verify
from articles.models import Article
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# 회원가입, 정보수정
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user


# 인증번호 대조
class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    verify_code = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        verify_code = data.get("verify_code")
        access = get_object_or_404(Verify, email=email)
        if verify_code == access.athnt_code:
            return data


# 마이페이지의 팔로잉 리스트
class FollowListSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id")
    nickname = serializers.CharField()
    profile_image = serializers.ImageField()

    class Meta:
        model = User
        fields = ["user_id", "nickname", "profile_image"]


# 마이페이지의 게시글
class UserArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


# 마이페이지용
class UserPageSerializer(serializers.ModelSerializer):
    user_articles = UserArticlesSerializer(many=True, read_only=True)
    following_list = FollowListSerializer(many=True, read_only=True)
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "nickname",
            "last_login",
            "profile_image",
            "following_count",
            "followers_count",
            "following_list",
            "user_articles",
        ]

    def get_followers_count(self, obj):
        return obj.following.count()

    def get_following_count(self, obj):
        return obj.following_list.count()


# 로그인용
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["nickname"] = user.nickname
        return token


# 프로필이미지
class UserProfileImageSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField()

    class Meta:
        model = User
        fields = [
            "profile_image",
        ]
