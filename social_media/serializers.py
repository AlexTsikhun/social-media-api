from django.contrib.auth import get_user_model
from rest_framework import serializers

from social_media import services
from social_media.models import Profile, Like, Post, Follow, Comment


class ProfileSerializer(serializers.ModelSerializer):
    # profile_name = serializers.CharField(source="user.username", read_only=True)
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
        )

    def get_is_liked(self, obj) -> bool:
        """Checks if `request.user` liked (`obj`) post."""
        user = self.context.get("request").user
        return services.is_liked(obj, user)


class PostListSerializer(serializers.ModelSerializer):
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
        )

    def get_is_liked(self, obj) -> bool:
        """Checks if `request.user` liked (`obj`) post."""
        user = self.context.get("request").user
        return services.is_liked(obj, user)


class LikeSerializer(serializers.ModelSerializer):
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
    comments = serializers.SerializerMethodField()
    likes = LikeSerializer(many=True, read_only=True)
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
            "total_likes",
            "likes",
            "total_comments",
            "comments",
            # "is_liked",
        )

    def get_comments(self, post):
        comments = post.user.comments.filter(post=post.id)
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            # "user",
            # "post",
            "comment_text",
            "comment_date",
            # ?
        )


class CommentListSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source="post.title", read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "post_title",
            "comment_text",
            "comment_date",
            # ?
        )


class CommentDetailSerializer(serializers.ModelSerializer):
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
    pass


class FollowListSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(source="follower.username", read_only=True)
    followed = serializers.CharField(source="followed.username", read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "follower", "followed", "created_at")
