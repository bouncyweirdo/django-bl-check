from __future__ import absolute_import

from celery import Celery

# instantiate Celery object
app = Celery(include=['blacklist_check.tasks'], broker='redis://localhost:6379/0')

# Optional configuration, see the application user guide.

# import celery config file
app.config_from_object('blacklist_check.celeryconfig')

app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()
