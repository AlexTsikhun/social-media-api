from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import generics, mixins, views
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from social_media.mixins import LikedMixin
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
    # PostListSerializer,
)


class RetrieveProfile(generics.ListAPIView):
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


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        # if self.action == "list":
        #     return PostListSerializer

        if self.action == "retrieve":
            return PostDetailSerializer

        if self.action == "add_comment":
            return CommentSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    @action(detail=True, methods=["post"], url_path="follow")
    def follow_user(self, request, pk=None):
        post = self.get_object()
        author = post.user

        follower = request.user
        followee = author

        if follower == followee:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Follow.objects.filter(follower=follower, followed=followee).exists():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Follow.objects.create(follower=follower, followed=followee)
        return Response(
            {"detail": "Successfully followed user."}, status=status.HTTP_201_CREATED
        )


class CommentViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return CommentListSerializer

        if self.action == "retrieve":
            return CommentDetailSerializer

        if self.action == "follow_user":
            return EmptySerializer

        return self.serializer_class

    @action(detail=True, methods=["post"], url_path="follow")
    def follow_user(self, request, pk=None):
        comment = self.get_object()
        author = comment.post.user

        follower = request.user
        followee = author

        if follower == followee:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Follow.objects.filter(follower=follower, followed=followee).exists():
            return Response(
                {"detail": "You are already following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Follow.objects.create(follower=follower, followed=followee)
        return Response(
            {"detail": "Successfully followed user."}, status=status.HTTP_201_CREATED
        )


class LikeViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):  #!!!!
        if self.action == "list":
            return CommentListSerializer

        if self.action == "retrieve":
            return CommentDetailSerializer

        return self.serializer_class


class FollowingViewSet(
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
            return CommentDetailSerializer

        return self.serializer_class


class AddCommentView(APIView):
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


# class FollowUserView(generics.CreateAPIView):
#     serializer_class = FollowSerializer
#     # permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         followee_id = request.data.get("followee_id")
#         if followee_id:
#             follower = request.user
#             followee = get_object_or_404(User, id=followee_id)
#
#             # Check if the user is already following the followee
#             if Follower.objects.filter(follower=follower, followee=followee).exists():
#                 return Response(
#                     {"detail": "You are already following this user."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#
#             Follower.objects.create(follower=follower, followee=followee)
#             return Response(
#                 {"detail": "Successfully followed user."},
#                 status=status.HTTP_201_CREATED,
#             )
#         else:
#             return Response(
#                 {"detail": "followee_id must be provided."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#
# class UnfollowUserView(generics.DestroyAPIView):
#     queryset = Follower.objects.all()
#     serializer_class = FollowerSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def delete(self, request, *args, **kwargs):
#         followee_id = kwargs.get("followee_id")
#         follower = request.user
#         followee = get_object_or_404(User, id=followee_id)
#
#         # Check if the user is following the followee
#         instance = get_object_or_404(Follower, follower=follower, followee=followee)
#         self.perform_destroy(instance)
#         return Response(
#             {"detail": "Successfully unfollowed user."},
#             status=status.HTTP_204_NO_CONTENT,
#         )
