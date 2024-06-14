from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from features.models import Post, Comment, Like, Follow
from features.serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
    FollowSerializer,
)

POST_URL = reverse("features:post-list")
COMMENT_URL = reverse("features:comment-list")
LIKE_URL = reverse("features:like-list")
FOLLOW_URL = reverse("features:follow-list")


def sample_post(author, **params):
    defaults = {
        "content": "Sample content",
    }
    defaults.update(params)
    return Post.objects.create(author=author, **defaults)


def sample_comment(author, post, **params):
    defaults = {
        "content": "Sample comment",
    }
    defaults.update(params)
    return Comment.objects.create(author=author, post=post, **defaults)


def sample_like(user, post):
    return Like.objects.create(user=user, post=post)


def sample_follow(follower, followed):
    return Follow.objects.create(follower=follower, followed=followed)


class UnauthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required_post(self):
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_comment(self):
        res = self.client.get(COMMENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_like(self):
        res = self.client.get(LIKE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_required_follow(self):
        res = self.client.get(FOLLOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_create_post(self):
        payload = {
            "content": "New post content",
        }
        res = self.client.post(POST_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=res.data["id"])
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.content, payload["content"])

    def test_list_posts(self):
        sample_post(author=self.user, content="Post 1")
        sample_post(author=self.user, content="Post 2")

        res = self.client.get(POST_URL)

        posts = Post.objects.order_by("id")
        serializer = PostSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_posts_by_author(self):
        another_user = get_user_model().objects.create_user(
            "other@test.com", "password123"
        )
        post1 = sample_post(author=self.user, content="Post 1")
        post2 = sample_post(author=another_user, content="Post 2")

        res = self.client.get(POST_URL, {"author": self.user.id})

        serializer1 = PostSerializer(post1)
        serializer2 = PostSerializer(post2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_create_comment(self):
        post = sample_post(author=self.user)
        payload = {
            "content": "New comment content",
            "post": post.id,
        }
        res = self.client.post(COMMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get(id=res.data["id"])
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, payload["content"])

    def test_list_comments(self):
        post = sample_post(author=self.user)
        sample_comment(author=self.user, post=post, content="Comment 1")
        sample_comment(author=self.user, post=post, content="Comment 2")

        res = self.client.get(COMMENT_URL)

        comments = Comment.objects.order_by("id")
        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_comments_by_author(self):
        post = sample_post(author=self.user)
        another_user = get_user_model().objects.create_user(
            "other@test.com", "password123"
        )
        comment1 = sample_comment(author=self.user, post=post, content="Comment 1")
        comment2 = sample_comment(author=another_user, post=post, content="Comment 2")

        res = self.client.get(COMMENT_URL, {"author": self.user.id})

        serializer1 = CommentSerializer(comment1)
        serializer2 = CommentSerializer(comment2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_create_like(self):
        post = sample_post(author=self.user)
        payload = {
            "post": post.id,
        }
        res = self.client.post(LIKE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        like = Like.objects.get(id=res.data["id"])
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, post)

    def test_list_likes(self):
        post = sample_post(author=self.user)
        sample_like(user=self.user, post=post)

        res = self.client.get(LIKE_URL)

        likes = Like.objects.order_by("id")
        serializer = LikeSerializer(likes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_likes_by_user(self):
        post = sample_post(author=self.user)
        another_user = get_user_model().objects.create_user(
            "other@test.com", "password123"
        )
        like1 = sample_like(user=self.user, post=post)
        like2 = sample_like(user=another_user, post=post)

        res = self.client.get(LIKE_URL, {"user": self.user.id})

        serializer1 = LikeSerializer(like1)
        serializer2 = LikeSerializer(like2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_create_follow(self):
        another_user = get_user_model().objects.create_user(
            "other@test.com", "password123"
        )
        payload = {
            "follower": another_user.id,
        }
        res = self.client.post(FOLLOW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        follow = Follow.objects.get(id=res.data["id"])
        self.assertEqual(follow.follower, self.user)
        self.assertEqual(follow.followed, another_user)

    def test_already_following(self):
        another_user = get_user_model().objects.create_user(
            "other@test.com", "password123"
        )
        payload = {
            "follower": another_user.id,
        }
        res = self.client.post(FOLLOW_URL, payload)
        res_new = self.client.post(FOLLOW_URL, payload)
        self.assertEqual(res_new.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res_new.data["detail"], "Already following")

    def test_list_follows(self):
        another_user = get_user_model().objects.create_user(
            "other@test.com", "password123"
        )
        sample_follow(follower=self.user, followed=another_user)

        res = self.client.get(FOLLOW_URL)

        follows = Follow.objects.order_by("id")
        serializer = FollowSerializer(follows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_follows_by_follower(self):
        another_user = get_user_model().objects.create_user(
            "other@test.com", "password123"
        )
        follow1 = sample_follow(follower=self.user, followed=another_user)
        follow2 = sample_follow(follower=another_user, followed=self.user)

        res = self.client.get(FOLLOW_URL, {"follower": self.user.id})

        serializer1 = FollowSerializer(follow1)
        serializer2 = FollowSerializer(follow2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
