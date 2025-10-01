from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token

from posts.models import Post
from rest_framework.test import APITestCase

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testusesr",
                                   password="1234567",
                                   email="testuser@gmail")

    def test_post_content(self):
        post = Post.objects.create(author=self.user, title="Test Title", content="Test Content")
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.content, "Test Content")


class PostAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser",
                                   password="1234567",
                                   email="testuser@gmail")
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

    def test_post_creation(self):
        post_data = {"title": "Test Title", "content": "Test Content"}
        response = self.client.post("/api/list-create/", post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, "Test Title")


