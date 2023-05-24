from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User
from users.serializers import UserSerializer, UserTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


# 회원가입
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
            )


# 로그인
class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, user_id):
        following_user = get_object_or_404(User, id=user_id)          # 내가 팔로우 하려는 유저
        user = request.user                                   # 나
        if user in following_user.following.all():
            following_user.following.remove(user)
            return Response({"message": "팔로우 취소"}, status=status.HTTP_200_OK)
        else:
            following_user.following.add(user)
            return Response({"message": "팔로우"}, status=status.HTTP_200_OK)
