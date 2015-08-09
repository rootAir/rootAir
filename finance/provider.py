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
from .type_launch import TypeLaunch


class Provider(models.Model):
    # id = models.IntegerField(primary_key=True)  # AutoField?
    description = models.CharField(max_length=100, unique=True)
    date_last_purchase = models.DateField('date last purchase')
    total_debit_week = models.DecimalField(max_digits=8, decimal_places=2)
    total_credit_week = models.DecimalField(max_digits=8, decimal_places=2)
    type_launch = models.ForeignKey(TypeLaunch, blank=True, null=True)
    synchronized = models.CharField(max_length=1, choices=STATUS_CHOICES)
    observation = models.TextField(help_text='') #blank=True, null=True

    def __unicode__(self):
        return self.type_launch

    def __str__(self):
        return self.description

    class Meta:
        # managed = False
        db_table = 'finance_provider'

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

    def __init__(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        super(Provider, self).__init__(*args, **kwargs)

    def provider_update(self, json_ext):
        """
        :param json_ext:
        :return:
        """
        launch = json_ext['launch']
        date = datetime.strptime(json_ext['date_purchase'], '%Y-%m-%dT%H:%M:%S').date()
        num_week = date.isocalendar()[1]
        if not Provider.objects.filter(description=launch).exists():
            pv = Provider()
        else:
            pv = Provider.objects.get(description=launch)

        pv.description = launch
        pv.date_last_purchase = date
        pv.total_debit_week = json_ext['value_debit']
        pv.total_credit_week = json_ext['value_credit']
        if pv.type_launch_id is None:
            # pv.type_launch_id  = self.set_provider_type(pv, json_ext)
            pv.type_launch_id = TypeLaunch.objects.get(type_name= settings.TYPELAUNCH_DEFAULT).id
        pv.num_week_id = num_week
        pv.save()
        return pv.id

    def set_provider_type(self, pv, json_ext):
        """
        :param pv:
        :param json_ext:
        :return:
        """
        _type = TypeLaunch.objects.all()
        for t in _type:
            print("Codigo = " + str(t.id) + " type = " + t.type_name)
        desc = 'Inform type to: ' + pv.description
        name_day = DayL[pv.date_last_purchase.weekday()]
        name_day += " day " + str(pv.date_last_purchase.day) + " " + pv.date_last_purchase.strftime("%B")
        desc += ' last date: ' + name_day
        desc += ' debit week: ' + str(json_ext['value_debit'])
        desc += ' credit week: ' + str(json_ext['value_credit']) + " => "
        n = input(desc)
        while not TypeLaunch.objects.filter(id=n).exists():
            n = input(desc)
        return n