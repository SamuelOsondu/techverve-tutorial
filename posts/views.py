from django.db.models import Count, Avg, Q, Case, Value, When
from rest_framework import generics
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post
from posts.serializers import PostSerializer
from .tasks import send_email_task

class PostAPIView(APIView):
    def get(self, request):
        serializer = PostSerializer(Post.objects.all(), many=True)

        return Response({"posts": serializer.data})


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['author', 'title']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Post.objects.select_related('author').annotate(
            num_comments=Count('comments'),
            popularity = Case(
                When(num_comments__gt=2, then=Value("medium")),
                When(num_comments__gt=5, then=Value("high")),
                When(num_comments__lt=2, then=Value("low")),
                default=Value("low")

            )
        ).all()

class PostRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionError("You can't edit someone else's post")
        serializer.save()
        return Response({"success": "Post updated successfully"})

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionError("You can't delete someone else's post")
        instance.delete()
        return Response({"success": "Post deleted successfully"})


class CustomAuthObtain(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk})

class PostStats(APIView):
    def get(self, request):
        posts = Post.objects.aggregate(
            total_posts=Count('id', distinct=True),
            average_comments=Avg('comments__id'),
            posts_count_with_comments=Count('id', filter=Q(comments__isnull=False), distinct=True)
        )
        return Response({"stats": posts})


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    user_name = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    user = User.objects.create_user(user_name, email, password)
    user.save()

    send_email_task.delay(user_name, email)

    return Response("User created successfully!")
