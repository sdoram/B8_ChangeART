from django.urls import path
from articles import views

urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home_view"),
    path("newpost/", views.ArticleView.as_view(), name="article_create_view"),
    path("<int:article_id>/", views.ArticleView.as_view(), name="article_detail_view"),
    path(
        "<int:article_id>/like/",
        views.ArticleLikeView.as_view(),
        name="article_like_view",
    ),
    path(
        "<int:article_id>/comment/",
        views.CommentView.as_view(),
        name="comment_create_view",
    ),
    path("comment/<int:comment_id>/", views.CommentView.as_view(), name="comment_view"),
    path("change/", views.ChangePostView.as_view(), name="change_post_view"),
]
