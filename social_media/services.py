from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from .models import Like


def add_like(obj, user):
    """Likes `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        user=user,
        content_type=obj_type,
        object_id=obj.id,
    )
    return like


def remove_like(obj, user):
    """Delete like from `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()


def is_fan(obj, user) -> bool:
    """Checking if `user` likes `obj`."""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_fans(obj):
    """List of all users that likes `obj`."""
    obj_type = ContentType.objects.get_for_model(obj)
    return get_user_model().objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id
    )
