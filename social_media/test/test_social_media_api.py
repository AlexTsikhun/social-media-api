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

        self.assertIn("comment_text", response.data)
        self.assertEqual(response.data["comment_text"], "This is a test comment")
        self.assertEqual(
            response.data["user"], self.user_commenter.username
        )  # Ensure comment is added by user_commenter

        # Check if the comment is shown in the post detail
        post_url = f"/api/v1/social_media/posts/{self.post.id}/"
        response = self.client.get(post_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("comments", response.data)
        self.assertEqual(len(response.data["comments"]), 1)
        self.assertEqual(
            response.data["comments"][0]["comment_text"], "This is a test comment"
        )
        self.assertEqual(
            response.data["comments"][0]["user"], self.user_commenter.username
        )

    def test_add_comment_invalid_post(self):
        comment_data = {"comment_text": "This is a test comment"}
        url = reverse(
            "social_media:add-comment-to-sb", kwargs={"post_id": self.post.id + 1}
        )
        response = self.client.post(url, comment_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Post not found")

    def test_add_comment_missing_comment_text(self):
        comment_data = {}
        url = reverse(
            "social_media:add-comment-to-sb", kwargs={"post_id": self.post.id}
        )

        response = self.client.post(url, comment_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("comment_text", response.data)
        self.assertEqual(
            "This field may not be null.", response.data["comment_text"][0]
        )


class AuthenticatedToggleLikeApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="email@gmail.com", password="password"
        )
        self.post = Post.objects.create(title="Test Post", user=self.user)

    def test_toggle_like_successful_add(self):
        url = reverse("social_media:toggle-like-for-sb", args=[self.post.id])
        self.client.force_authenticate(user=self.user)

        # Create a mock for services.add_like using create_autospec
        add_like = mock.create_autospec(services.add_like)

        # Patch services.add_like with the mock
        with patch.object(services, "add_like", add_like):
            # Mock services.is_liked to return False (user has not liked the post)
            with patch.object(services, "is_liked", return_value=False):
                response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Like added successfully")

        # Verify that services.add_like was called once with the correct arguments
        add_like.assert_called_once_with(self.post, self.user)

    def test_toggle_like_successful_remove(self):
        url = reverse("social_media:toggle-like-for-sb", args=[self.post.id])
        self.client.force_authenticate(user=self.user)

        remove_like = mock.create_autospec(services.remove_like)
        with patch.object(services, "remove_like", remove_like):
            with patch.object(services, "is_liked", return_value=True):
                response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Like removed successfully")

        remove_like.assert_called_once_with(self.post, self.user)

    def test_toggle_like_post_not_found(self):
        url = reverse("social_media:toggle-like-for-me", args=[999])
        self.client.force_authenticate(user=self.user)

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Post not found")

    def test_toggle_like_unauthenticated(self):
        url = reverse("social_media:toggle-like-for-me", args=[self.post.id])

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserCreationTests(TestCase):
    """when create user - create profile, test signal"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_and_profile(self):
        user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(reverse("user:create"), user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

        user = User.objects.get(username="testuser")
        self.assertTrue(Profile.objects.filter(user=user).exists())


# comme view
