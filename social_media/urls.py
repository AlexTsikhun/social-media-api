from django.urls import path, include
from rest_framework import routers

from social_media.views import (
    # ProfileViewSet,
    PostViewSet,
    CommentViewSet,
    RetrieveProfileAPIView,
    UserPostsViewSet,
    AddCommentAPIView,
    FollowingViewSet,
    ToggleLikeAPIView,
    FollowersViewSet,
    UpdateProfileAPIView,
)

app_name = "social_media"

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

profile_router = routers.DefaultRouter()
profile_router.register("user-posts", UserPostsViewSet)
profile_router.register("user-comments", CommentViewSet)
profile_router.register("user-following", FollowingViewSet, basename="user-following")
profile_router.register("user-followers", FollowersViewSet, basename="user-followers")

urlpatterns = [
    path("", include(router.urls)),
    path("profile/", RetrieveProfileAPIView.as_view()),
    path("profile/<int:user_id>/", UpdateProfileAPIView.as_view()),
    path("profile/", include(profile_router.urls)),
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
