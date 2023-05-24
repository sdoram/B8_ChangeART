from rest_framework import serializers
from .models import User
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


class UserArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


# 마이페이지용
class UserPageSerializer(serializers.ModelSerializer):
    user_articles = UserArticlesSerializer(many=True, read_only=True)


    class Meta:
        model = User
        fields = ["email", "nickname", "last_login", "profile_image", "user_articles"]


# 로그인용
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token
