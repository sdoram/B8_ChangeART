from django.urls import path, include
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup_view"),
    path("login/", views.LoginView.as_view(), name="login_view"),
]
