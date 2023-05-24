from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import User
from users.serializers import (
    UserSerializer,
    UserTokenObtainPairSerializer,
    UserPageSerializer,
)
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


# 마이페이지
class MyPageView(APIView):
    # 내 정보보기
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        # print(user)
        # articles = user.articles.all()
        serializer = UserPageSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 내 정보 수정
    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "수정이 되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    # 회원탈퇴
    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            user.is_active = False
            user.save()
            return Response({"message": "탈퇴하셨습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "권한이 없습니다"}, status=status.HTTP_400_BAD_REQUEST)


# 팔로우
# class FollowView(APIView):
#     def post(self, request, user_id):
#         user = get_object_or_404(User, id=user_id)
#         follow_list = user.following_list.all()
#         if request.user in follow_list:
#             follow_list.delete(request.user)
#             return Response({"message": "팔로우를 취소했습니다!"}, status=status.HTTP_200_OK)
#         elif request.user not in follow_list:
#             follow_list.save(request.user)
#             return Response({"message": "팔로우를 눌렀습니다!"}, status=status.HTTP_200_OK)
#         elif request.user == user_id:
#             return Response(
#                 {"message": "자신은 팔로우 할 수 없습니다!"}, status=status.HTTP_400_BAD_REQUEST
#             )
