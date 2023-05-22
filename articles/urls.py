from django.urls import path
from articles import views

urlpatterns = [
    path("<int:article_id>/comment", views.CommentView.as_view()),
    path("comment/<int:comment_id>", views.CommentView.as_view()),
]
