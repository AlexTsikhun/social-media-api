from datetime import datetime

from rest_framework import generics, pagination
from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework import generics, mixins, views
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from social_media import services
from social_media.mixins import (
    FollowMixin,
    UnfollowMixin,
)
from social_media.models import Profile, Post, Like, Follow, Comment
from social_media.permissions import IsAuthorOrReadOnly
from social_media.serializers import (
    MyProfileSerializer,
    PostSerializer,
    CommentSerializer,
    CommentListSerializer,
    PostDetailSerializer,
    CommentDetailSerializer,
    LikeSerializer,
    FollowSerializer,
    FollowingListSerializer,
    EmptySerializer,
    FollowingDetailSerializer,
    PostListSerializer,
    CommentProfileSerializer,
    CommentListProfileSerializer,
    FollowerDetailSerializer,
    FollowerListSerializer,
    ProfileSerializer,
    # ProfileImageSerializer,
    MyProfileSerializer,
    # PostListSerializer,
)


class RetrieveProfileAPIView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """ListAPIView with user filtering - like RetrieveAPIView (detail url not suitable)"""
        return self.queryset.filter(user=self.request.user)


class UpdateProfileAPIView(generics.UpdateAPIView):
    """No need to override get_queryset bc it's profile page"""

    queryset = Profile.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    lookup_field = "user_id"


class UserPostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.request.user.id)

        post_title = self.request.query_params.get("title")
        post_date = self.request.query_params.get("post_date")

        if post_title:
            queryset = queryset.filter(title__icontains=post_title)

        if post_date:
            departure_time = datetime.strptime(post_date, "%Y-%m-%d").date()
            queryset = queryset.filter(post_date__date=departure_time)

        return queryset.order_by("id")

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_serializer_class(self):
        # if self.action == "list":
        #     return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        if self.action == "add_comment":
            return CommentSerializer

        return self.serializer_class


class PostViewSet(FollowMixin, UnfollowMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_permissions(self):
        if self.action in ["follow_post_author", "unfollow_post_author"]:
            return (IsAuthenticated(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        if self.action == "add_comment":
            return CommentSerializer

        if self.action in ["follow_post_author", "unfollow_post_author"]:
            return EmptySerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    @action(detail=True, methods=["post"], url_path="follow")
    def follow_post_author(self, request, pk=None):
        post = self.get_object()
        author = post.user
        return self._follow_author(request, author)

    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow_post_author(self, request, pk=None):
        post = self.get_object()
        author = post.user
        return self._unfollow_author(request, author)

    @action(detail=True, methods=["get"])
    def redirect_to_profile(self, request, pk=None):
        post = self.get_object()
        user_username = post.user.username
        profile_url = f"/api/v1/social_media/profile/{user_username}"
        return redirect(profile_url)


class FollowingViewSet(
    FollowMixin,
    UnfollowMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        """Username filtering by followee"""

        username = self.kwargs["username"]
        queryset = self.queryset.filter(follower__username=username)

        username = self.request.query_params.get("username")

        if username:
            queryset = queryset.filter(followee__username__icontains=username)

        return queryset.order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return FollowingListSerializer

        if self.action == "retrieve":
            return FollowingDetailSerializer

        if self.action in ["follow_user", "unfollow_user"]:
            return EmptySerializer

        return self.serializer_class

    @action(detail=True, methods=["post"], url_path="follow")
    def follow_user(self, request, pk=None, **kwargs):
        follow = self.get_object()
        user = follow.followee
        return self._follow_author(request, user)

    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow_user(self, request, pk=None, **kwargs):
        follow = self.get_object()
        user = follow.followee
        return self._unfollow_author(request, user)

    @action(detail=True, methods=["get"])
    def redirect_to_profile(self, request, pk=None, **kwargs):
        follow = self.get_object()
        user_username = follow.followee.username
        profile_url = f"/api/v1/social_media/profile/{user_username}"
        return redirect(profile_url)


class MyProfileFollowingViewSet(FollowingViewSet):
    def get_queryset(self):
        """Username filtering by followee"""
        queryset = self.queryset.filter(follower=self.request.user)

        username = self.request.query_params.get("username")

        if username:
            queryset = queryset.filter(followee__username__icontains=username)

        return queryset.order_by("id")


class FollowersViewSet(
    FollowMixin,
    UnfollowMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = self.queryset.filter(followee__username=username)

        username = self.request.query_params.get("username")

        if username:
            queryset = queryset.filter(follower__username__icontains=username)

        return queryset.order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return FollowerListSerializer

        if self.action == "retrieve":
            return FollowerDetailSerializer

        if self.action in ["follow_user", "unfollow_user"]:
            return EmptySerializer

        return self.serializer_class

    @action(detail=True, methods=["post"], url_path="follow")
    def follow_user(self, request, pk=None, **kwargs):
        follow = self.get_object()
        user = follow.follower
        return self._follow_author(request, user)

    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow_user(self, request, pk=None, **kwargs):
        follow = self.get_object()
        user = follow.follower
        return self._unfollow_author(request, user)

    @action(detail=True, methods=["get"])
    def redirect_to_profile(self, request, pk=None, **kwargs):
        follow = self.get_object()
        user_username = follow.follower.username
        profile_url = f"/api/v1/social_media/profile/{user_username}"
        return redirect(profile_url)


class MyProfileFollowersViewSet(FollowersViewSet):

    def get_queryset(self):
        queryset = self.queryset.filter(followee=self.request.user)

        username = self.request.query_params.get("username")

        if username:
            queryset = queryset.filter(follower__username__icontains=username)

        return queryset.order_by("id")


class CommentViewSet(
    FollowMixin,
    UnfollowMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Comment.objects.all()
    serializer_class = CommentProfileSerializer
    permission_classes = (IsAuthenticated,)  # for enter profile - it should be user

    def get_permissions(self):
        """write this method to explicitly, it no mandatory"""
        if self.action in ["follow_post_author", "unfollow_post_author"]:
            return (IsAuthenticated(),)
        return super().get_permissions()

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        post_title = self.request.query_params.get("post_title")

        if post_title:
            queryset = queryset.filter(post__title__icontains=post_title)

        return queryset.order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListProfileSerializer

        if self.action == "retrieve":
            return CommentDetailSerializer

        if self.action in ["follow_post_author", "unfollow_post_author"]:
            return EmptySerializer

        return self.serializer_class

    @action(detail=True, methods=["post"], url_path="follow")
    def follow_post_author(self, request, pk=None):
        comment = self.get_object()
        author = comment.post.user
        return self._follow_author(request, author)

    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow_post_author(self, request, pk=None):
        comment = self.get_object()
        author = comment.post.user
        return self._unfollow_author(request, author)

    @action(detail=True, methods=["get"])
    def redirect_to_profile(self, request, pk=None):
        comment = self.get_object()
        user_username = comment.post.user.username
        profile_url = f"/api/v1/social_media/profile/{user_username}"
        return redirect(profile_url)


class AddCommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        comment_data = {
            "user": request.user,
            "post": post,
            "comment_text": request.data.get("comment_text"),
        }
        serializer = CommentSerializer(data=comment_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ToggleLikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if services.is_liked(post, request.user):
            services.remove_like(post, request.user)
            return Response(
                {"message": "Like removed successfully"}, status=status.HTTP_200_OK
            )
        services.add_like(post, request.user)

        return Response(
            {"message": "Like added successfully"}, status=status.HTTP_200_OK
        )


class ProfileDetailView(generics.RetrieveAPIView):
    """Only for view other profiles (not to follow, RetrieveProfileAPIView doesn't support)"""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)
    # lookup_field = "username"

    def get_object(self):
        username = self.kwargs["username"]
        return self.get_queryset().get(user__username=username)
