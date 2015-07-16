from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import *
import os
from django.conf import settings
from utils.util import *
from django.db import transaction
from finance.type_launch import TypeLaunch

GROUP_CHOICES = (
    ('Task', 'Task'),
    ('Sport', 'Sport'),
    ('Fun', 'Fun'),
    ('Study', 'Study'),
    ('Person', 'Person'),
)

class TypeActivity(models.Model):
    # id = models.IntegerField(primary_key=True)  # AutoField?
    type_name = models.CharField(max_length=10, unique=True)
    type_desc = models.CharField(max_length=50)
    group = models.CharField(max_length=10, choices=GROUP_CHOICES)
    positive = models.BooleanField(default=False, db_index=True)
    type_launch = models.ForeignKey(TypeLaunch, blank=True, null=True)
    synchronized = models.CharField(max_length=1, choices=STATUS_CHOICES)

    # def __unicode__(self):
    #     return u'%s' % (self.type_name)
    def __str__(self):
        """
        :return:
        """
        return self.type_desc

    class Meta:
        # managed = False
        db_table = 'activity_typeactivity'

    def save(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        if settings.DATABASE_LOCAL:
            self.synchronized = 'L'  #local
        else:
            self.synchronized = 'H'  #heroku
        super(self.__class__, self).save(*args, **kwargs)


