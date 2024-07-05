from rest_framework import routers
from django.urls import path, include
from rest_framework_nested import routers as nested_routers

from social_media.views import (
    # ProfileViewSet,
    PostViewSet,
    CommentViewSet,
    RetrieveProfile,
    UserPostsViewSet,
    AddCommentView,
    FollowingViewSet,
)

app_name = "social_media"

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

r = routers.DefaultRouter()
r.register("user-posts", UserPostsViewSet)
r.register("user-comments", CommentViewSet)
r.register("user-following", FollowingViewSet)
# r.register("add-like", UserPostsViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("profile/", include(r.urls)),
    path("profile/", RetrieveProfile.as_view()),
    path(
        "profile/user-posts/<int:post_id>/add_comment/",
        AddCommentView.as_view(),
        name="add-comment",
    ),
    path(
        "posts/<int:post_id>/add_comment/",
        AddCommentView.as_view(),
        name="add-comment",
    ),
]
# how to delete user from serializer - use perform create
# all posts, followed posts
