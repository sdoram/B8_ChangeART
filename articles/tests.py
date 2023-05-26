from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

# 임시 이미지 생성용 패키지
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile


# 임시 이미지 생성
def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, "png")
    return temp_file


class HomeViewTest(APITestCase):
    pass


class ArticleViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("article@test.com", "테스트", "1234")
        cls.login_data = {"email": "article@test.com", "password": "1234"}
        cls.article_data = {"title": "게시글 제목", "content": "게시글 내용"}

    def setUp(self):
        self.access_token = self.client.post(
            reverse("login_view"), self.login_data
        ).data["access"]

    def test_create_fail_article(self):
        url = reverse("article_create_view")
        response = self.client.post(url, self.article_data)
        self.assertEqual(response.status_code, 401)

    def test_create_success_article(self):
        response = self.client.post(
            path=reverse("article_create_view"),
            data=self.article_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data["message"], "게시글을 등록했습니다.")

    def test_create_article_with_image(self):
        # 임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        self.article_data["image"] = image_file
        # 전송
        response = self.client.post(
            path=reverse("article_create_view"),
            data=encode_multipart(data=self.article_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.data["message"], "게시글을 등록했습니다.")


class ArticleLikeViewTest(APITestCase):
    pass


class CommentViewTest(APITestCase):
    pass


class ChangePostViewTest(APITestCase):
    pass
