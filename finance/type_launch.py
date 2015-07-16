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


class TypeLaunch(models.Model):
    # id = models.IntegerField(primary_key=True)  # AutoField?
    type_name = models.CharField(max_length=100, unique=True)
    cost_fixo = models.BooleanField(default=False, db_index=True)
    investment = models.BooleanField(default=False, db_index=True)
    value_fixed = models.DecimalField(max_digits=8, decimal_places=2)
    synchronized = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self):
        return self.type_name

    class Meta:
        managed = False
        db_table = 'finance_typelaunch'

    def save(self, *args, **kwargs):
        if settings.DATABASE_LOCAL:
            self.synchronized = 'L'  #local
        else:
            self.synchronized = 'H'  #heroku
        super(self.__class__, self).save(*args, **kwargs)