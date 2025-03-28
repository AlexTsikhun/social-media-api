import os

from celery import Celery
from django.apps import apps
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_api.settings")

app = Celery("social_media_api")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.

# show all tasks in drop down menu
app.config_from_object(settings)
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

# @app.task(bind=True, ignore_result=True)
# def debug_task(self):
#     print(f"Request: {self.request!r}")
