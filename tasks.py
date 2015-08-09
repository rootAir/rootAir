# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import Celery, shared_task
from datetime import datetime
# import pika, os, logging
# logging.basicConfig()
from django.conf import settings
# try:
#     from celery.task import task
# except ImportError:
#     from celery.decorators import task
import os
import time
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
app = Celery('tasks', backend="amqp", broker='')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
from utils.sync_report import *
from utils.graphic import *
# from broker.sync_mycap import SyncMycap
from finance.sync_itau import SyncItau
from utils.sync_db import SyncDb
from utils.sync_report import SyncReport


class SyncMycap(SyncMycap):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class SyncItau(SyncItau):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class SyncDb(SyncDb):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


# @shared_task
@app.task  #(queue='sync_mycap')
def sync_mycap():
    if settings.DATABASE_LOCAL:
        sync_mycap = SyncMycap()
        sync_mycap.run()

@app.task  #(queue='sync_itau')
def sync_itau():
    if settings.DATABASE_LOCAL:
        sync_itau = SyncItau()
        sync_itau.run()

@app.task  #(queue='sync_db')
def sync_db():
    if settings.DATABASE_LOCAL:
        sync_db = SyncDb()
        sync_db.run()

# @shared_task
@app.task  #(queue='sync_report')
def sync_report():
    _report = SyncReport()
    _report.sync_report()

