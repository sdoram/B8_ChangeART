from django.urls import reverse
from rest_framework.test import APITestCase

from .models import User, Verify


# 인증코드 발송
class AthntCodeCreateViewTest(APITestCase):
    def test_send_success(self):
        url = reverse("athnt_code_create_view")
        data = {"email": "test@test.com"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)


# 회원가입
class SignupViewTest(APITestCase):
    def setUp(self):
        self.email = {"email": "signup@test.com"}
        self.url = reverse("athnt_code_create_view")
        self.response = self.client.post(self.url, self.email)
        self.verify = Verify.objects.get(email=self.email["email"])

    def test_signup_success(self):
        url = reverse("signup_view")
        user_data = {
            "email": "signup@test.com",
            "nickname": "테스트",
            "password": "1234",
            "verify_code": self.verify.athnt_code,
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)


# 로그인
class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "login@test.com",
            "테스트",
            "1234",
        )
        self.login_data = {
            "email": "login@test.com",
            "password": "1234",
        }

    def test_login(self):
        response = self.client.post(reverse("login_view"), self.login_data)
        self.assertEqual(response.status_code, 200)
