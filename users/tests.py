from django.urls import reverse
from rest_framework.test import APITestCase

from .models import User, Verify


class AthntCodeCreateViewTest(APITestCase):
    def test_send_email(self):
        url = reverse("athnt_code_create_view")
        data = {"email": "test@test.com"}

        response = self.client.post(url, data)
        self.assertEqual(response.data["message"], "이메일을 보냈습니다.")


class SignupViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = {"email": "signup@test.com"}
        cls.url = reverse("athnt_code_create_view")

    def setUp(self):
        self.response = self.client.post(self.url, self.email)
        self.verify = Verify.objects.get(email=self.email["email"])

    def test_signup(self):
        url = reverse("signup_view")
        user_data = {
            "email": "signup@test.com",
            "nickname": "테스트",
            "password": "1234",
            "verify_code": self.verify.athnt_code,
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.data["message"], "가입완료!")


class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("login@test.com", "테스트", "1234")
        self.login_data = {"email": "login@test.com", "password": "1234"}

    def test_login(self):
        response = self.client.post(reverse("login_view"), self.login_data)
        self.assertEqual(response.status_code, 200)


class MyPageViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("login@test.com", "테스트", "1234")
        cls.login_data = {"email": "login@test.com", "password": "1234"}
        cls.put_data = {"nickname": "프로필 수정", "password": "change1234"}

    def setUp(self):
        self.access_token = self.client.post(
            reverse("login_view"), self.login_data
        ).data["access"]

    def test_get_user(self):
        response = self.client.get(path=reverse("my_page_view", args=[self.user.id]))
        self.assertEqual(response.data["nickname"], "테스트")

    def test_put_user(self):
        response = self.client.put(
            path=reverse("my_page_view", args=[self.user.id]),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.put_data,
        )
        self.assertEqual(response.data["message"], "수정이 되었습니다.")

    def test_delete_user(self):
        response = self.client.delete(
            path=reverse("my_page_view", args=[self.user.id]),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data["message"], "탈퇴하셨습니다")


class FollowViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.from_user = User.objects.create_user("following@test.com", "팔로잉", "1234")
        cls.to_user = User.objects.create_user("follow@test.com", "팔로우", "1234")
        cls.from_user_data = {"email": "following@test.com", "password": "1234"}
        cls.to_user_data = {"email": "follow@test.com", "password": "1234"}

    def setUp(self):
        self.from_user_access_token = self.client.post(
            reverse("login_view"), self.from_user_data
        ).data["access"]

    def test_follow_user(self):
        response = self.client.post(
            path=reverse("follow_view", args=[self.to_user.id]),
            HTTP_AUTHORIZATION=f"Bearer {self.from_user_access_token}",
        )
        self.assertEqual(response.data["message"], "팔로우했습니다")

    def test_un_follow_user(self):
        for _ in range(2):
            response = self.client.post(
                path=reverse("follow_view", args=[self.to_user.id]),
                HTTP_AUTHORIZATION=f"Bearer {self.from_user_access_token}",
            )
        self.assertEqual(response.data["message"], "팔로우를 취소했습니다")
