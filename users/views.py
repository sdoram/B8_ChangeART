from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from .serializers import UserSerializer, UserTokenObtainPairSerializer

from .models import User, Verify
from users.serializers import (
    UserSerializer,
    UserTokenObtainPairSerializer,
    UserPageSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import EmailMessage
from random import randint


# 인증코드 생성 & 이메일 발송
class AthntCodeCreateView(APIView):
    def post(self, request):
        email = request.data.get("email", "")
        athnt_code = str(randint(1, 999999)).zfill(6)

        message = EmailMessage(
            "ChangeART [Verification Code]",
            athnt_code,
            "changeart@gmail.com",
            [email],
        )
        authen_Code = Verify(email=email, athnt_code=athnt_code)
        authen_Code.save()
        message.send()
        return Response({"message": "이메일을 보냈습니다."}, status=status.HTTP_200_OK)


# 이메일 인증
class EmailAccessView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data["email"])
            if user.ahtnt_code == request.data["code"]:
                user.is_active = True
                user.save()
                return Response({"message": "이메일 인증 성공"}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"message": "이메일 인증 실패"}, status=status.HTTP_400_BAD_REQUEST
            )


# 회원가입
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_vaild()
        serializer.save()
        return Response({"message": "가입완료!"}, status=status.HTTP_201_CREATED)


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
            return Response({"message": "탈퇴하셨습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "권한이 없습니다"}, status=status.HTTP_400_BAD_REQUEST)
