from rest_framework.views import APIView


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
