from django.contrib import admin

from social_media.models import Post, Comment, Profile

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Profile)
