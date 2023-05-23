from .models import Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CommentSerializer
from rest_framework.generics import get_object_or_404


class ArticleView(APIView):
    def get(self, request, article_id):
        """상세 게시글 보기"""
        pass

    def post(self, request):
        """게시글 작성"""
        pass

    def put(self, request, article_id):
        """게시글 수정"""
        pass

    def delete(self, request, article_id):
        """게시글 삭제"""
        pass


class CommentView(APIView):
    def post(self, request, article_id):
        """댓글을 작성합니다."""
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=request.user,
            article=get_object_or_404(Article, pk=article_id),
        )
        return Response({"message": "post 요청 성공"})

    def put(self, request, comment_id):
        """댓글을 수정합니다."""
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.user:
            serializer = CommentSerializer(comment)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "put 요청 성공"})
        else:
            return Response({"message": "delete 요청 실패"})

    def delete(self, request, comment_id):
        """댓글을 삭제합니다."""
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message": "delete 요청 성공"})
        else:
            return Response({"message": "delete 요청 실패"})
