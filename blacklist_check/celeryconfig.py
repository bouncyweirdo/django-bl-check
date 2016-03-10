from __future__ import absolute_import
import django
import os

from celery import Celery
from django.conf import settings

# instantiate Celery object
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django.conf:settings')
django.setup()

app = Celery(include=['blacklist_check.tasks'], broker='redis://localhost:6379/0')

# Optional configuration, see the application user guide.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
