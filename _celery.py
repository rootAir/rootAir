from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('tasks', broker='amqp://plkzskqc:-DQxz-O9tlCfXtuZgwCvMVtM9ouw4Wu9@hyena.rmq.cloudamqp.com/plkzskqc')

# instantiate Celery object
# app = Celery(include=[ 'finance.tasks' ])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# import celery config file
# celery.config_from_object('celeryconfig')

# if __name__ == '__main__':
#     celery.start()

# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# app.conf.update(
#     CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
# )
# app.conf.update(
#     CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
# )

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))


# celery.config_from_object('celeryconfig')