from django.contrib.auth import get_user_model
from rest_framework import serializers

from social_media import services
from social_media.models import Profile, Like, Post, Follow, Comment
from user.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    # profile_name = serializers.CharField(source="user.username", read_only=True)
    user = serializers.CharField(source="user.username", read_only=True)
    my_posts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "bio",
            "user",
            "profile_picture",
            "registration_date",
            "last_login",
            "my_posts",
        )

    def get_my_posts(self, profile):
        posts = profile.user.posts.all()
        serializer = PostSerializer(posts, many=True)
        return serializer.data


class PostSerializer(serializers.ModelSerializer):
    # add post instance
    # is_liked = serializers.SerializerMethodField()
    # total_comments = serializers.IntegerField(
    #     source="airplane.all_places", read_only=True
    # )
    user = serializers.CharField(source="user.username", read_only=True)
        is_following_author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "image",
            "content",
            "post_date",
            "total_likes",
            "total_comments",
            # "is_liked",
            "is_following_author",
        )

    def get_is_liked(self, obj) -> bool:
        """Checks if `request.user` liked (`obj`) post."""
        user = self.context.get("request").user
        return services.is_liked(obj, user)

    def get_is_following_author(self, obj):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None

        if obj.user == user:
            return "it's me"

        if user and user.is_authenticated:
            return Follow.objects.filter(follower=user, followed=obj.user).exists()
        return False


class PostListSerializer(PostSerializer):
    # add post instance
    # is_liked = serializers.SerializerMethodField()
    # total_comments = serializers.IntegerField(
    #     source="airplane.all_places", read_only=True
    # )
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "image",
            "content",
            "post_date",
            "total_likes",
            "total_comments",
            # "is_liked",
            "is_following_author",
        )

    def get_is_liked(self, obj) -> bool:
        """Checks if `request.user` liked (`obj`) post."""
        user = self.context.get("request").user
        return services.is_liked(obj, user)


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Like
        fields = (
            "id",
            "user",
            "like_date",
            # ?
        )


class PostDetailSerializer(PostSerializer):
    # add post instance
    # is_liked = serializers.SerializerMethodField()
    user = serializers.CharField(source="user.username", read_only=True)
    comments = serializers.SerializerMethodField()
    likes = LikeSerializer(many=True, read_only=True)
    is_following_author = serializers.SerializerMethodField()

    # likes?

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "title",
            "image",
            "content",
            "post_date",
            "is_following_author",
            "likes",
            "total_comments",
            "comments",
            # "is_liked",
        )

    def get_comments(self, post):
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def get_likes(self, post):
        likes = post.user.comments.filter(post=post.id)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    # def get_is_liked(self, obj) -> bool:
    #     """Checks if `request.user` liked (`obj`) post."""
    #     user = self.context.get("request").user
    #     return services.is_liked(obj, user)

    def get_is_following_author(self, obj):
        request = self.context.get("request")
        user = request.user if request and hasattr(request, "user") else None

        if obj.user == user:
            return "it's me"

        if user and user.is_authenticated:
            return Follow.objects.filter(follower=user, followed=obj.user).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    # this should remove
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "comment_text",
            "comment_date",
        )


class CommentProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            # "post",
            "comment_text",
            "comment_date",
            # ?
        )


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    post_title = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "post_title",
            "comment_text",
            "comment_date",
        )


class CommentListProfileSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "post_title",
            "comment_text",
            "comment_date",
        )


class CommentDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    # post_title = serializers.CharField(source="post.title", read_only=True)
    post = PostListSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "post",
            "comment_text",
            "comment_date",
            # ?
        )


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "follower", "followed", "created_at")


class EmptySerializer(serializers.Serializer):
    """Serializer for click actions(follow)"""

    pass


class FollowListSerializer(serializers.ModelSerializer):
    # follower = serializers.CharField(source="follower.username", read_only=True)
    followed = serializers.CharField(source="followed.username", read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "followed", "created_at")


class FollowDetailSerializer(serializers.ModelSerializer):
    # follower = serializers.CharField(source="follower.username", read_only=True)
    followed = UserSerializer(
        many=False, read_only=True
    )  # ProfileSerializer(many=False, read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "followed", "created_at")
