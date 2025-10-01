from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    num_comments = serializers.IntegerField(read_only=True)
    popularity = serializers.CharField(read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'author', "num_comments", "popularity"]
