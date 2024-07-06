from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import generics, mixins, views
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from social_media import services
from social_media.mixins import (
    LikedMixin,
    FollowMixin,
    UnfollowMixin,
)
from social_media.models import Profile, Post, Like, Follow, Comment
from social_media.serializers import (
    ProfileSerializer,
    PostSerializer,
    CommentSerializer,
    CommentListSerializer,
    PostDetailSerializer,
    CommentDetailSerializer,
    LikeSerializer,
    FollowSerializer,
    FollowListSerializer,
    EmptySerializer,
    FollowDetailSerializer,
    PostListSerializer,
    CommentProfileSerializer,
    CommentListProfileSerializer,
    # PostListSerializer,
)


class RetrieveProfile(generics.ListAPIView, generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """ListAPIView with user filtering - like RetrieveAPIView (detail url not suitable)"""
        return self.queryset.filter(user=self.request.user)


class UserPostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

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
    # permission_classes = (IsAuthenticatedOrReadOnly,)

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


class CommentViewSet(
    FollowMixin,
    UnfollowMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Comment.objects.all()
    serializer_class = CommentProfileSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

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


class FollowingViewSet(
    FollowMixin,
    UnfollowMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    # permission_classes = (IsAuthenticatedOrReadOnly,)
    # following list filtered show id for all user, I need personal (and comment)
    def get_queryset(self):
        return self.queryset.filter(follower=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return FollowListSerializer

        if self.action == "retrieve":
            return FollowDetailSerializer

        if self.action in ["follow_user", "unfollow_user"]:
            return EmptySerializer

        return self.serializer_class

    @action(detail=True, methods=["post"], url_path="follow")
    def follow_user(self, request, pk=None):
        follow = self.get_object()
        user = follow.followee
        return self._follow_author(request, user)

    @action(detail=True, methods=["post"], url_path="unfollow")
    def unfollow_user(self, request, pk=None):
        follow = self.get_object()
        user = follow.followee
        return self._unfollow_author(request, user)


class AddCommentAPIView(APIView):
    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)
            comment = Comment.objects.create(
                user=request.user,
                post=post,
                comment_text=request.data.get("comment_text"),
            )
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToggleLikeAPIView(APIView):
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
