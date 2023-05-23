from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from articles.models import Article
from articles.serializers import ArticleCreateSerializer, ArticleDetailSerializer


class ArticleView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]
    # 얘네 쓰면 편하지만 그럼 상세게시글 보기에도 적용이 됨 고민중 -> OrReadOnly로 시도

    def get(self, request, article_id):
        """상세 게시글 보기"""
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """게시글 작성"""
        serializer = ArticleCreateSerializer(data=request.data)

        # if not request.user.is_authenticated:
        #     return Response(
        #         {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
        #     )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "게시글을 등록했습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, article_id):
        """게시글 수정"""
        article = get_object_or_404(Article, id=article_id)

        # if not request.user.is_authenticated:
        #     return Response(
        #         {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
        #     )

        if request.user == article.user:
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response({"message": "게시글이 수정되었습니다."}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("본인만 수정할 수 있습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id):
        """게시글 삭제"""
        article = get_object_or_404(Article, id=article_id)

        # if not request.user.is_authenticated:
        #     return Response(
        #         {"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED
        #     )

        if request.user == article.user:
            article.delete()
            return Response(
                {"message": "게시글이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT
            )
        else:
            return Response("작성자만 삭제할 수 있습니다.", status=status.HTTP_403_FORBIDDEN)


class ArticleLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        """좋아요"""
        if request.user in article.like.all():
            article.like.remove(request.user)
            return Response({"message": "좋아요를 취소했습니다."}, status=status.HTTP_200_OK)
        else:
            article.like.add(request.user)
            return Response({"message": "좋아요를 했습니다."}, status=status.HTTP_200_OK)
