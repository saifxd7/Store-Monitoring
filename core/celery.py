from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")
app.config_from_object(settings, namespace="CELERY")

# # # Using Redis as the message broker
# app.conf.broker_url = 'redis://127.0.0.1:6379/0'
# app.conf.result_backend = 'redis://127.0.0.1:6379/0'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# celery -A core worker --pool=solo -l info
