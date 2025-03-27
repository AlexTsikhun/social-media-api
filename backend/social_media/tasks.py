from celery import shared_task
from social_media.models import Post
from user.models import User


@shared_task
def create_post(user_id, title, content):
    user = User.objects.get(pk=user_id)
    post = Post.objects.create(user=user, title=title, content=content)
    return post.id
