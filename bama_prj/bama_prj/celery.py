"""import docstring """
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bama_prj.settings')

APP = Celery('bama_prj')
APP.config_from_object('django.conf:settings', namespace='CELERY')
APP.autodiscover_tasks()

APP.conf.update(
    result_expires=60,
    task_acks_late=True,
    broker_url='pyamqp://localhost',
    result_backend='db+postgresql://postgres:post@51136616@localhost:5433/bama_prj'
)
