from rest_framework import status
from rest_framework.response import Response

from social_media.models import Follow


class FollowMixin:
    def _follow_author(self, request, author):
        follower = request.user
        followee = author

        if follower == followee:
            return Response(
                {"detail": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Follow.objects.filter(follower=follower, followee=followee).exists():
            return Response(
                {"detail": "You are already following this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Follow.objects.create(follower=follower, followee=followee)
        return Response(
            {"detail": "Successfully followed user"}, status=status.HTTP_201_CREATED
        )


class UnfollowMixin:
    def _unfollow_author(self, request, author):
        follower = request.user
        followee = author

        if not Follow.objects.filter(follower=follower, followee=followee).exists():
            return Response(
                {"detail": "You are not following this user"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        Follow.objects.filter(follower=follower, followee=followee).delete()
        return Response(
            {"detail": "Successfully unfollowed user"},
            status=status.HTTP_204_NO_CONTENT,
        )
