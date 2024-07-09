from django.urls import path, include
from rest_framework import routers

from social_media.views import (
    # ProfileViewSet,
    PostViewSet,
    CommentViewSet,
    RetrieveProfileAPIView,
    UserPostsViewSet,
    AddCommentAPIView,
    MyProfileFollowingViewSet,
    ToggleLikeAPIView,
    MyProfileFollowersViewSet,
    UpdateProfileAPIView,
    ProfileDetailView,
    FollowingViewSet,
    FollowersViewSet,
)

app_name = "social_media"

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

my_profile_router = routers.DefaultRouter()
my_profile_router.register("user-posts", UserPostsViewSet)
my_profile_router.register("user-comments", CommentViewSet)
my_profile_router.register(
    "user-following", MyProfileFollowingViewSet, basename="user-following"
)
my_profile_router.register(
    "user-followers", MyProfileFollowersViewSet, basename="user-followers"
)

profile_router = routers.DefaultRouter()
profile_router.register("following", FollowingViewSet, basename="user-following")
profile_router.register("followers", FollowersViewSet, basename="user-followers")

urlpatterns = [
    path("", include(router.urls)),
    path("my-profile/", RetrieveProfileAPIView.as_view()),
    path("my-profile/<int:user_id>/", UpdateProfileAPIView.as_view()),
    path("my-profile/", include(my_profile_router.urls)),
    path(
        "my-profile/user-posts/<int:post_id>/add_comment/",
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
        "my-profile/user-posts/<int:post_id>/like/",
        ToggleLikeAPIView.as_view(),
        name="add-like",
    ),
    path(
        "profile/<str:username>/",
        ProfileDetailView.as_view(),
        name="profile-detail",
    ),
    path("profile/<str:username>/", include(profile_router.urls)),
]
