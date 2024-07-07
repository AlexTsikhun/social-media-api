from rest_framework import routers
from django.urls import path, include
from rest_framework_nested import routers as nested_routers

from social_media.views import (
    # ProfileViewSet,
    PostViewSet,
    CommentViewSet,
    RetrieveProfile,
    UserPostsViewSet,
    AddCommentAPIView,
    FollowingViewSet,
    ToggleLikeAPIView,
    FollowersViewSet,
)

app_name = "social_media"

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

r = routers.DefaultRouter()
r.register("user-posts", UserPostsViewSet)
r.register("user-comments", CommentViewSet)
r.register("user-following", FollowingViewSet, basename="user-following")
r.register("user-followers", FollowersViewSet, basename="user-followers")
# r.register("add-like", UserPostsViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("profile/", RetrieveProfile.as_view()),
    path("profile/", include(r.urls)),
    path(
        "profile/user-posts/<int:post_id>/add_comment/",
        AddCommentAPIView.as_view(),
        name="add-comment",
    ),
    path(
        "posts/<int:post_id>/add_comment/",
        AddCommentAPIView.as_view(),
        name="add-comment",
    ),
    path(
        "posts/<int:post_id>/like/",
        ToggleLikeAPIView.as_view(),
        name="add-like",
    ),
    path(
        "profile/user-posts/<int:post_id>/like/",
        ToggleLikeAPIView.as_view(),
        name="add-like",
    ),
]
