from django.urls import path
from posts.views import PostAPIView, PostListCreateView, PostRetrieveUpdateDestroyView, CustomAuthObtain, PostStats, \
    register_user

urlpatterns = [
    path('posts/', PostAPIView.as_view(), name='posts'),
    path("list-create/", PostListCreateView.as_view(), name="list-create"),
    path("detail/<int:pk>/", PostRetrieveUpdateDestroyView.as_view(), name="detail"),
    path("token/", CustomAuthObtain.as_view(), name="token"),
    path("stats/", PostStats.as_view(), name="stats"),

    path("register/", register_user, name="register")
]

