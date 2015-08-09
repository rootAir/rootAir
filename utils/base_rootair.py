# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import *
from .util import *
from django.db.models import Sum, Max
from django.contrib import messages
from django.db import transaction
from django.conf import settings
import os
from finance.extract import Extract
# from broker.investment import Investment


class BaseRootAir(models.Model):

    class Meta:
        abstract = True

    def __unicode__(self):
        return u"%s" % (self.id or 'Not Saved')

    @property
    def ssr_workflow_status(self):
        return self.sr_workflow_status(sr_type='SSR')

    def clean_synchronized(self):
        if self.instance:
            return self.instance.synchronized
        else:
            return self.fields['synchronized']

    def save(self, *args, **kwargs):
        if settings.DATABASE_LOCAL:
            self.synchronized = 'L'  #local
        else:
            self.synchronized = 'H'  #heroku
        super(self.__class__, self).save(*args, **kwargs)

