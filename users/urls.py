from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup_view"),
    path("login/", views.LoginView.as_view(), name="login_view"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("mypage/<int:user_id>/", views.MyPageView.as_view(), name="my_page_view"),
    # path("<int:user_id>/", views.FollowView.as_view(), name="follow_view"),
]
