import os
import tempfile
from datetime import datetime

from PIL import Image
from django.contrib.auth import get_user_model
from django.db.models import F, Count
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from social_media.models import Profile, Post
from social_media.serializers import PostListSerializer
from user.models import User

# PROFILE_URL = reverse("social_media_api:profile")
MY_PROFILE_URL = reverse("social_media:my-profile")
USER_POSTS_URL = reverse("social_media:user-posts-list")


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


def my_profile_detail_url(my_profile_id):
    return reverse("social_media:profile-detail", args=[my_profile_id])


class UnauthenticatedApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(USER_POSTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedUserPostsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test_username",
            "test@test1.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    # filter by post name
    def test_list_user_posts(self):
        user1 = sample_user(username="username_test2", email="email@gmail1.com")
        # user2 = sample_user(username="username_test2", email="email@gmail.com")
        sample_post(user=user1)
        sample_post(user=user1, title="My title2")

        # why res is empty??
        res = self.client.get(USER_POSTS_URL)

        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
