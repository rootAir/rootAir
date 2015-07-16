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
from finance.provider import Provider


class Balance(models.Model):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

    #@transaction.non_atomic_requests(using=settings.DATABASE_REMOTE)
    #@transaction.commit_on_success
    def save(self, json=None):
        """
        :param json:
        :return:
        """
        ds_local = _class.objects.all()
        ds = _class()
        for loc in ds_local:
            for field in loc.__dict__:
                if field != '_state':
                    ds.__dict__[field] = loc.__dict__[field]
            ds.save()

        print('Sincronized %s execution in %s'%(str(ds),_time))
        sys.stdout.flush()
        #transaction.commit()


class Extract(models.Model):
    # id = models.IntegerField(primary_key=True)  # AutoField?
    date_launch = models.DateField('date launch')
    launch = models.CharField(max_length=100)
    date_purchase = models.DateField('date purchase')
    value_debit = models.DecimalField(max_digits=8, decimal_places=2)
    value_credit = models.DecimalField(max_digits=8, decimal_places=2)
    value_balance = models.DecimalField(max_digits=8, decimal_places=2)
    cancelled = models.BooleanField(default=True, db_index=True)
    provider = models.ForeignKey(Provider, blank=True, null=True)
    #provider = models.IntegerField(blank=True, null=True)
    synchronized = models.CharField(max_length=1, choices=STATUS_CHOICES)

    class Meta:
        managed = True
        db_table = 'finance_extract'

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

    _line_head = 2
    # def __init__(self, *args, **kwargs):
    #     super(Extract, self).__init__(*args, **kwargs)

    # @transaction.commit_on_success
    def save_ext(self, json_ext=None):
        """
        :param json_ext:
        :return:
        """
        try:
            # super(self.__class__, json_ext)
            pv = Provider()
            for ext in json_ext:
                prov_id = pv.provider_update(ext)
                if bool(prov_id):
                    _ext = Extract()
                    _ext.date_launch = datetime.strptime(ext['date_launch'], '%Y-%m-%dT%H:%M:%S').date()
                    _ext.launch = ext['launch']
                    _ext.date_purchase = datetime.strptime(ext['date_purchase'], '%Y-%m-%dT%H:%M:%S').date()
                    _ext.value_debit = ext['value_debit']
                    _ext.value_credit = ext['value_credit']
                    _ext.value_balance = ext['value_balance']
                    _ext.cancelled = ext['cancelled']
                    _ext.provider_id = prov_id
                    _ext.synchronized = 'L'
                    _ext.save()
        except:
            print('erro save json extract')
        #     transaction.rollback()
        # else:
        #     transaction.commit()

    def get_cost_month(self, matrix, _week, type_launch):
        """
        :param matrix:
        :param _week:
        :param type_launch:
        :return:
        """
        line = 0
        matrix[line].append('debit week %s' %_week.num_week)

        line += 1
        for lf in type_launch:
            cost_week = self.get_total_week(_week, lf.id)
            if cost_week.__len__() > 1:
                value_debit = cost_week[0]
                value_credit = cost_week[1]
                matrix[line].append(str(value_credit-value_debit).replace('.',','))
            else:
                matrix[line].append('0')
            line += 1
        return matrix

    def get_cost_week(self, matrix, date):
        """
        :param matrix:
        :param date:
        :return:
        """
        extract = Extract.objects.filter(
                                            date_purchase=date,
                                            provider__type_launch__cost_fixo=False,
                                            provider__type_launch__investment=False
                                        )
        day_cost = 0
        for launch in extract:
            day_cost += launch.value_debit

        line = 0
        day_name = name_day(date)
        matrix[line].append(day_name)
        matrix[line].append(str(day_cost).replace('.',','))
        matrix[line].append('Type')

        line = 1
        for cost in extract:
            matrix[line].append(cost.launch)
            matrix[line].append(str(cost.value_debit).replace('.',','))
            matrix[line].append(self.name_cost(cost.launch))
            line += 1

        while line < matrix.__len__():
            matrix[line].append('')
            matrix[line].append('')
            matrix[line].append('')
            line += 1
        return matrix

    def name_cost(self, launch):
        """
        :param launch:
        :return:
        """
        name_cost = Provider.objects.get(description=launch).type_launch.type_name
        return name_cost

    def get_total_week(self, week, _type=None, _fixed=False, _invest=False):
        """
        :param week:
        :param _type:
        :param _fixed:
        :param _invest:
        :return:
        """
        value_week = []
        tot_debit_week = 0
        tot_credit_week = 0
        tot_week_before = 0
        extracts = Extract.objects.filter(
                                            date_purchase__range=[week.date_init, week.date_final],
                                            provider__type_launch__cost_fixo=_fixed,
                                            provider__type_launch__investment=_invest
                                        )
        if not _type is None:
            extracts = extracts.filter(provider__type_launch_id=_type)

        if extracts.exists():
            for extract in extracts:
                tot_debit_week += extract.value_debit
                tot_credit_week += extract.value_credit
            value_week.append(tot_debit_week)
            value_week.append(tot_credit_week)
            value_week.append(tot_credit_week - tot_debit_week)
            value_week.append(tot_week_before)
        else:
            value_week = [self._line_head]
        return value_week

    def get_date_purchase(self, date_launch, launch):
        """
        :param date_launch:
        :param launch:
        :return:
        """
        launch = launch.strip()
        if launch[-3] == '/':
            date_purchase = launch[-5:].replace('/','-')
            year = date_launch.year
            if date_purchase[-2:] == '12' and date_launch.month == 1:
                year = date_launch.year - 1

            # incorrect file extract itau
            if int(date_purchase[-2:]) > 12:
                date_purchase = date_purchase[:3] + '%02d' %date_launch.month

            date_purchase += '-' + str(year)
            date_purchase = datetime.strptime(date_purchase, '%d-%m-%Y').date()

            # previous launch the previous week
            if (date_launch.isocalendar()[1] - date_purchase.isocalendar()[1]) > 1:
                date_purchase = date_launch
        else:
            date_purchase = date_launch

        return date_purchase

    def importer_extract(self, _file):
        """
        :param _file:
        :return:
        """
        try:
            _extract = []
            contents = _file.readlines()
            line = 0
            while line < len(contents):
                _date_launch, _launch, _value = str(contents[line], 'utf-8').split(';')
                _extract += self.extract_exists(_date_launch, _launch, _value)
                line += 1
            _file.close()

            if _extract.__len__() > 0:
                self.save_ext(_extract)
            return _extract
        except Exception:
            print("error or file extract Itau week imported not found.")

    def extract_exists(self, _date_launch, _launch_dt, _value):
        """
        :param _date_launch:
        :param _launch_dt:
        :param _value:
        :return:
        """
        try:
            _list_extract = []
            _date_launch = str_to_date(_date_launch)
            _launch = self.get_launch(_launch_dt)
            _date_purchase = self.get_date_purchase(_date_launch, _launch_dt)
            _value = str_to_float(_value)
            if _value < 0:
                _value_debit = abs(_value)
                _value_credit = 0
            else:
                _value_debit = 0
                _value_credit = _value

            extract = Extract.objects.filter(launch=_launch, date_purchase=_date_purchase)
            if _value < 0:
                _extract = extract.filter(value_debit=abs(_value))
            else:
                _extract = extract.filter(value_credit=_value)

            if not _extract.exists():
                _list_extract.append({
                                "date_launch": _date_launch.strftime('%Y-%m-%dT%H:%M:%S'),
                                "launch": _launch,
                                "date_purchase": _date_purchase.strftime('%Y-%m-%dT%H:%M:%S'),
                                "value_debit": str(_value_debit).replace('\'','\'\''),
                                "value_credit": str(_value_credit),
                                "value_balance": str(0),
                                "cancelled": str(1),
                                "provider": str(None)
                            })
        except:
            print('Erro function is_equal in extract.')
            pass
        return _list_extract

    def get_launch(self, launch):
        """
        :param launch:
        :return:
        """
        launch = launch.strip()
        if launch[-3] == '/':
            launch = launch[:-6].strip()
        return launch