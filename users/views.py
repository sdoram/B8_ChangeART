from random import randint
from django.core.mail import EmailMessage
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, UserTokenObtainPairSerializer
from .models import User, Verify
from users.serializers import (
    UserSerializer,
    UserTokenObtainPairSerializer,
    UserPageSerializer,
    VerifySerializer,
)


# 인증코드 생성 & 이메일 발송
class AthntCodeCreateView(APIView):
    def post(self, request):
        email = request.data.get("email", "")
        if User.objects.filter(email=email).exists():
            return Response(
                {"message": "이미 가입된 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST
            )
        code = Verify.objects.filter(email=email)
        if code.exists():
            code.delete()
        athnt_code = str(randint(1, 999999)).zfill(6)
        message = EmailMessage(
            "ChangeART [Verification Code]",
            f"인증코드 [{athnt_code}]",
            "HOST@gmail.com",
            [email],
        )
        authen_Code = Verify(email=email, athnt_code=athnt_code)
        authen_Code.save()
        message.send()
        return Response({"message": "이메일을 보냈습니다."}, status=status.HTTP_200_OK)


# 이메일 인증 & 회원가입
class SignupView(APIView):
    def post(self, request):
        Verify = VerifySerializer(data=request.data)
        if Verify.is_valid():
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {"message": f"${serializer.errors}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response({"message": "인증번호 불일치"}, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


# 마이페이지
class MyPageView(APIView):
    # 내 정보 보기
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
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
            return Response({"message": "탈퇴하셨습니다"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "권한이 없습니다"}, status=status.HTTP_400_BAD_REQUEST)


class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, user_id):
        following_user = get_object_or_404(User, id=user_id)  # 내가 팔로우 하려는 유저
        user = request.user  # 나
        if user in following_user.following.all():
            following_user.following.remove(user)
            return Response({"message": "팔로우를 취소했습니다"}, status=status.HTTP_200_OK)
        else:
            following_user.following.add(user)
            return Response({"message": "팔로우했습니다"}, status=status.HTTP_200_OK)
