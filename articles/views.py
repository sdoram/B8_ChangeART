from .models import Comment
from rest_framework.views import APIView
from rest_framework.response import Response


class CommentView(APIView):
    def post(self, request, article_id):
        """댓글을 작성합니다."""
        return Response({"message": "post 요청"})

    def put(self, request, comment_id):
        """댓글을 수정합니다."""
        return Response({"message": "put 요청"})

    def delete(self, request, comment_id):
        """댓글을 삭제합니다."""
        return Response({"message": "delete 요청"})
