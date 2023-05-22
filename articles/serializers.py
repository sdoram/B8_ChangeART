from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = "__all__"
