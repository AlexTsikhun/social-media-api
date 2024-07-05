from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from social_media import services
from social_media.models import Post, Comment
from user.serializers import UserSerializer


class LikedMixin:

    @action(methods=["POST"], detail=True)
    def like(self, request, pk=None):
        """Лайкает `obj`."""
        obj = self.get_object()  # return post model
        services.add_like(obj, request.user)
        return Response(
            {"message": "Like added successfully"},
            status=status.HTTP_200_OK,  # show inbrowsable panndel
        )

    @action(methods=["POST"], detail=True)
    def unlike(self, request, pk=None):
        """Удаляет лайк с `obj`."""
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response(
            {"message": "Like removed successfully"}, status=status.HTTP_200_OK
        )

    @action(methods=["GET"], detail=True)
    def likes(self, request, pk=None):
        """Получает всех пользователей, которые лайкнули `obj`."""
        obj = self.get_object()
        likes = services.get_likes(obj)
        serializer = UserSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True)
    def add_comment(self, request, pk=None):
        post = Post.objects.get(pk=pk)
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            comment_text=request.data.get("comment_text"),
        )
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
