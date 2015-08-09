# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import *
from .exceptions import IncorrectCellLabel
from utils.util import *
from django.db.models import Sum, Max
from django.contrib import messages
from django.db import transaction
from django.conf import settings
import os
from .provider import *


class Prevision(models.Model):
    # id = models.IntegerField(primary_key=True)  # AutoField?
    description = models.CharField(max_length=100, unique=True)
    date_expiration = models.DateField('date expiration')
    debit_prevision = models.DecimalField(max_digits=8, decimal_places=2)
    credit_prevision = models.DecimalField(max_digits=8, decimal_places=2)
    provider = models.ForeignKey(Provider, blank=True, null=True)
    date_payment = models.DateField('date payment', blank=True, null=True)
    synchronized = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, null=True)
    observation = models.TextField(help_text='') #blank=True, null=True
    paid = models.BooleanField(default=False, db_index=True)

    def __unicode__(self):
        return self.type_launch

    class Meta:
        # managed = False
        db_table = 'finance_prevision'

    def save(self, *args, **kwargs):
        if settings.DATABASE_LOCAL:
            self.synchronized = 'L'  #local
        else:
            self.synchronized = 'H'  #heroku
        if self.date_payment is None:
            self.paid = False
        else:
            self.paid = True
        super(self.__class__, self).save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super(Prevision, self).__init__(*args, **kwargs)