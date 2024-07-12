from rest_framework import serializers

from social_media import services
from social_media.models import Profile, Like, Post, Follow, Comment
from user.serializers import UserSerializer


class MyProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "bio",
            "user",
            "profile_picture",
            "total_followers",
            "total_followees",
            "total_posts",
            "registration_date",
            "last_login",
        )


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "bio",
            "user",
            "profile_picture",
            "total_followers",
            "total_followees",
            "registration_date",
            "last_login",
            "posts",
        )

    def get_posts(self, profile):
        posts = profile.user.posts.all()
        serializer = PostListSerializer(posts, many=True)
        return serializer.data


class PostSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
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
            "is_liked",
            "total_likes",
            "total_comments",
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
            return Follow.objects.filter(follower=user, followee=obj.user).exists()
        return False


class PostListSerializer(PostSerializer):
    is_liked = serializers.SerializerMethodField()
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
            "is_liked",
            "total_likes",
            "total_comments",
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
        )


class PostDetailSerializer(PostSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    comments = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    likes = LikeSerializer(many=True, read_only=True)
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
            "is_following_author",
            "is_liked",
            "likes",
            "total_comments",
            "comments",
        )

    def get_comments(self, post):
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

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
            return Follow.objects.filter(follower=user, followee=obj.user).exists()
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
            "comment_text",
            "comment_date",
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
    post = PostListSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "post",
            "comment_text",
            "comment_date",
        )


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "follower", "followee", "created_at")


class EmptySerializer(serializers.Serializer):
    """Serializer for click actions(follow)"""

    pass


class FollowingListSerializer(FollowSerializer):
    followee = serializers.CharField(source="followee.username", read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "followee", "created_at")


class FollowerListSerializer(FollowSerializer):
    follower = serializers.CharField(source="follower.username", read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "follower", "created_at")


class FollowingDetailSerializer(serializers.ModelSerializer):
    followee = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "followee", "created_at")


class FollowerDetailSerializer(serializers.ModelSerializer):
    follower = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "follower", "created_at")
