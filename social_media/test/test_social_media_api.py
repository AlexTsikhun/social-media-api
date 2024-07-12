import unittest.mock as mock
from datetime import datetime
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from social_media import services
from social_media.models import Profile, Post, Follow
from social_media.serializers import PostSerializer
from user.models import User

MY_PROFILE_URL = reverse("social_media:my-profile")
USER_POSTS_URL = reverse("social_media:user-posts-list")
POSTS_URL = reverse("social_media:posts-list")


def follow_post_author_url(post_id):
    return reverse("social_media:posts-list-follow", kwargs={"post_id": post_id})


def sample_user(**params):
    defaults = {
        "username": "test_username",
        "email": "test@test1.com",
        "password": "password123",
    }
    defaults.update(params)
    return User.objects.create(**defaults)


def sample_profile(**params):
    defaults = {
        # "user": user,
        "bio": "My bio",
    }
    defaults.update(params)
    return Profile.objects.create(**defaults)


def sample_post(**params):
    defaults = {
        "user": None,
        "title": "My title",
        "content": "My content",
    }
    defaults.update(params)
    return Post.objects.create(**defaults)


class UnauthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(USER_POSTS_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserPostsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="test_username",
            email="email@gmail1.com",
            password="testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_user_posts_with_all_fields(self):
        user = self.user
        sample_post(user=user)
        sample_post(user=user, title="My title2")

        response = self.client.get(USER_POSTS_URL)

        posts = Post.objects.all()
        serializer = PostSerializer(
            posts, many=True, context={"request": response.wsgi_request}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Post.objects.count())
        self.assertEqual(response.data, serializer.data)

        # Compare 'is_following_author' field in serializer with expected result
        for index, post_data in enumerate(response.data):
            expected_is_following_author = serializer.data[index]["is_following_author"]
            self.assertEqual(
                post_data["is_following_author"], expected_is_following_author
            )

    # another
    def test_create_post(self):
        user1 = self.user
        payload = {
            "user": user1.id,
            "title": "TItle",
            "content": "COntent",
        }
        response = self.client.post(POSTS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        post = Post.objects.get(id=response.data["id"])

        self.assertEqual(post.user, user1)
        self.assertIsInstance(post.user, get_user_model())
        self.assertIsNotNone(post.user)

    def test_filter_user_posts_by_post_date(self):
        user = self.user
        a1 = sample_post(user=user)
        a2 = sample_post(user=user, title="My title2")

        posts = Post.objects.filter(
            post_date__date=datetime.today().strftime("%Y-%m-%d")
        )

        response = self.client.get(
            USER_POSTS_URL,
            {"post_date": datetime.today().strftime("%Y-%m-%d")},
        )

        serializer = PostSerializer(
            posts, many=True, context={"request": response.wsgi_request}
        )
        self.assertEqual(serializer.data, response.data)

    def test_filter_flights_by_airplane_name(self):
        user = self.user
        a1 = sample_post(user=user)
        a2 = sample_post(user=user, title="My title2")

        posts = Post.objects.filter(title__icontains="2")

        response = self.client.get(
            USER_POSTS_URL,
            {"title": "2"},
        )

        serializer = PostSerializer(
            posts, many=True, context={"request": response.wsgi_request}
        )
        self.assertEqual(serializer.data, response.data)


class AuthenticatedPostsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_follower = User.objects.create_user(
            username="test_username",
            email="email@gmail1.com",
            password="<PASSWORD>",
        )
        self.user_post_creator = User.objects.create_user(
            username="test_username2",
            email="email@gmail2.com",
            password="<PASSWORD>",
        )
        self.client.force_authenticate(self.user_follower)
        self.post = Post.objects.create(
            title="My title",
            content="My content",
            user=self.user_post_creator,
        )

    def test_follow_post_author(self):
        url = f"/api/v1/social_media/posts/{self.post.pk}/follow/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unfollow_post_author(self):
        """First, make sure user2 is following user1 (post author)"""
        Follow.objects.get_or_create(
            follower=self.user_follower, followee=self.user_post_creator
        )

        url = f"/api/v1/social_media/posts/{self.post.pk}/unfollow/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_redirect_to_profile(self):
        url_redirect = f"/api/v1/social_media/posts/{self.post.pk}/redirect_to_profile/"
        response_redirect = self.client.get(url_redirect)

        # Assert that the response status code is 302 Found (redirect)
        self.assertEqual(response_redirect.status_code, status.HTTP_302_FOUND)

        self.assertTrue(
            response_redirect.url.endswith(
                f"/api/v1/social_media/profile/{self.user_post_creator.username}"
            )
        )


class AuthenticatedFollowingApiTests(TestCase):
    pass


class AuthenticatedAddCommentApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_poster = User.objects.create_user(
            username="poster",
            email="email@poster.com",
            password="testpass",
        )
        self.user_commenter = User.objects.create_user(
            username="commenter",
            email="email@commenter.com",
            password="testpass",
        )
        self.client.force_authenticate(self.user_commenter)
        self.post = Post.objects.create(
            title="My title",
            content="My content",
            user=self.user_poster,
        )

    def test_add_comment_success(self):
        comment_data = {"comment_text": "This is a test comment"}

        url = reverse(
            "social_media:add-comment-to-sb", kwargs={"post_id": self.post.id}
        )

        response = self.client.post(url, comment_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
