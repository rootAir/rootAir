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
from finance.extract import Extract
from broker.investment import Investment
from utils.dropbox import *
from django.core.files import File as FileWrapper
import xlrd, os
# from utils.base_rootair import BaseRootAir
# from build.billiard.Doc.includes.mp_synchronize import value_func


class WeekNumber(models.Model):    #BaseRootAir
    # id = models.IntegerField(primary_key=True)  # AutoField?
    num_week = models.IntegerField()
    date_closed = models.DateTimeField('date time closed', null=True, blank=True)
    value_week = models.DecimalField(max_digits=8, decimal_places=2)
    value_debit_week = models.DecimalField(max_digits=8, decimal_places=2)
    date_init = models.DateField('date initial week')
    date_final = models.DateField('date final week')
    value_credit_week = models.DecimalField(max_digits=8, decimal_places=2)
    close_week = models.BooleanField(default=False, db_index=True)
    value_invest = models.DecimalField(max_digits=8, decimal_places=2)
    value_transf = models.DecimalField(max_digits=8, decimal_places=2)
    value_trade = models.DecimalField(max_digits=8, decimal_places=2)
    docfile_mycap = models.FileField(upload_to='')
    docfile_itau = models.FileField(upload_to='')
    quant_trade = models.IntegerField()
    tax_trade = models.DecimalField(max_digits=8, decimal_places=2)
    percent_result = models.CharField(max_length=8, blank=True)
    synchronized = models.CharField(max_length=1, choices=STATUS_CHOICES)
    cost_fixed_week = models.DecimalField(max_digits=8, decimal_places=2)
    available_broker = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    operation_broker = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'finance_weeknumber'

    def save(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        self.docfile_mycap = send_file_dropbox(self.docfile_mycap)
        self.docfile_itau = send_file_dropbox(self.docfile_itau)
        if settings.DATABASE_LOCAL:
            self.synchronized = 'L'  #local
        else:
            self.synchronized = 'H'  #heroku
        super(self.__class__, self).save(*args, **kwargs)

    def consolidate_week(self):
        """
        :return:
        """
        _num_week_close = WeekNumber.objects.filter(close_week=True).order_by('-date_init')[0].num_week
        for _num_week in range(_num_week_close +1, this_week() +1):
            _week = self.get_or_create(_num_week, True)
        return _week

    def send_file_to_dropbox(self):
        """
        :return: buffering=-1, encoding="ISO-8859-1"
        _type_file = mycap or itau
        """
        try:
            _files_mycap = get_all_files(settings.DIR_LOCAL, '*.xls')
            if _files_mycap.__len__() > 0:
                _path_file = _files_mycap[0][1]
                _file = open(_path_file, 'rb')
                self.import_extract_mycap(_file)
                # if not self.import_exists(_path_file, 'mycap'):
                    # _week = self.get_or_create(None, True)
                    # remove_file_dropbox(_week.docfile_mycap.name.split('/')[-1])
                    # _week.docfile_mycap = send_file_dropbox(FileWrapper(_file))
                    # _week.save()

            _files_itau = get_all_files(settings.DIR_LOCAL, '*.txt')
            if _files_itau.__len__() > 0:
                _path_file = _files_itau[0][1]
                _file = open(_path_file, 'rb')
                self.import_extract_itau(_file)
                # if not self.import_exists(_path_file, 'itau'):
                #     _week = self.get_or_create(None, True)
                #     remove_file_dropbox(_week.docfile_itau.name.split('/')[-1])
                #     _week.docfile_itau = send_file_dropbox(FileWrapper(_file))
                #     _week.save()

            self.consolidate_week()
            remove_files_path()
        except:
            print('erro function get_file_to_dropbox')

    def import_exists(self, _path_file, _type):
        """
        :param _path_file:
        :param _type:
        :return:
        """
        try:
            _file = open(_path_file, 'rb')
            if _type == 'mycap':
                _invest = Investment()
                _workbook = xlrd.open_workbook(None, None, 0, 1, _file.read())
                _worksheet = _workbook.sheet_by_name('Sheet1')
                _last_row = _worksheet.row(1)
                _list = _invest.file_to_json(_last_row)[0]
                if _invest.is_extract_mycap(_worksheet) and not _invest.investment_exists(_list):
                    return False

            if _type == 'itau':
                _ext = Extract()
                contents = _file.readlines()
                _last_line = len(contents)
                _date_launch, _launch, _value = str(contents[_last_line - 1], 'utf-8').split(';')
                if not _ext.extract_exists(_date_launch, _launch, _value).__len__() == 0:
                    return False
            return True
        except:
            print('erro execution _file import_exists')

    def import_extract_itau(self, _file=None):
        """
        :return:
        """
        _ext = Extract()
        if _file is not None:
            _ext.importer_extract(_file)
        else:
            _week = self.get_or_create()
            if _week.docfile_itau.name != '':
                docfile_itau = get_file_dropbox(_week.docfile_itau)
                if docfile_itau:
                    _ext.importer_extract(docfile_itau)

    def import_extract_mycap(self, _file=None):
        """
        :return:
        """
        _invest = Investment()
        if _file is not None:
            _invest.import_extract_mycap(_file)
        else:
            _week = self.get_or_create()
            if _week.docfile_mycap.name != '':
                docfile_mycap = get_file_dropbox(_week.docfile_mycap)
                if docfile_mycap:
                    _invest.import_extract_mycap(docfile_mycap)

    def update_broker(self, _value_available):
        """
        :param _value_available:
        :return:
        """
        _num_week = this_week()
        _week = WeekNumber.objects.filter(num_week= _num_week)
        if _week.exists():
            _week = WeekNumber.objects.get(num_week= _num_week)
            _week.available_broker = _value_available
            _week.operation_broker = float(_week.value_invest) - _value_available
            _week.value_invest -= _week.operation_broker
            _week.save()

    # @transaction.set_autocommit
    def get_or_create(self, num_week=None, force=False):
        """
        :param num_week:
        :param force:
        :return:
        """
        # try:
        # analise erro value_invest e value_trade (negativo com erro)
        if num_week is None: num_week = this_week()
        week = WeekNumber.objects.filter(num_week=num_week)
        if not week.exists():
            week = WeekNumber()
        else:
            week = WeekNumber.objects.get(num_week=num_week)
        if not week.close_week or force:
            _invest = Investment()
            day_week = self.get_rang_week(num_week)[0]
            value_week = self.get_value_week(day_week)[0]
            week.num_week = num_week
            week.date_init = day_week['date_init']
            week.date_final = day_week['date_final']
            week.value_week = value_week['value_week']
            week.value_debit_week = value_week['value_debit_week']
            week.value_credit_week = value_week['value_credit_week']

            tax_trade = _invest.get_tax_trade(week)[0]
            _value_trade = _invest.get_value_trade(week)
            result_mycap = _value_trade - tax_trade['tax_trade']
            _value_invest = value_week['value_invest_before'] + value_week['value_transf'] + result_mycap
            week.value_invest = _value_invest
            week.value_transf = value_week['value_transf']
            week.value_trade = result_mycap
            week.quant_trade = tax_trade['quant_trade']
            week.tax_trade = tax_trade['tax_trade']
            week.cost_fixed_week = self.get_cost_fixed_week(day_week['date_init'])

            _total_week = week.value_week + _value_invest
            _total_week_before = value_week['value_week_before'] + value_week['value_invest_before']
            week.percent_result = to_percent((_total_week / _total_week_before) - 1)

            _dt = Extract.objects.aggregate(Max('date_purchase'))
            if _dt['date_purchase__max'] > day_week['date_final']:
                week.close_week = True
                week.date_closed = str_to_datetime()
            else:
                week.close_week = False
            week.save()
        # except:
        #     print('erro function get_or_create!')
        #     pass
        #     transaction.rollback()
        # else:
        #     transaction.commit()
        return week

    def get_cost_fixed_week(self, _date=None):  # Rateio cost fixed in month
        """
        :param _date:
        :return:  _week.date_init ration quantity week in month
        """
        import calendar
        _value_week = 0
        if _date is None:
            _date = datetime.today().date()
        _month = str(_date.month)
        _year = str(_date.year)
        _last_day_month = str(calendar.monthrange(_date.year, _date.month)[1])
        _date_init = datetime.strptime('01-%s-%s' %(_month, _year) , '%d-%m-%Y').date()
        _date_final = datetime.strptime('%s-%s-%s' %(_last_day_month, _month, _year) , '%d-%m-%Y').date()

        _extracts = Extract.objects.filter(
                                            date_purchase__range=[_date_init, _date_final],
                                            provider__type_launch__cost_fixo=True,
                                            provider__type_launch__investment=False
                                        )
        for _deb in _extracts:
            _value_week += _deb.value_debit
        _value_week = float(round(_value_week / 4, 2))

        return _value_week

    def get_value_week_before(self, date):
        """
        :param date:
        :return:
        """
        value_week_before = 0
        num_week = self.dif_date(1, date).isocalendar()[1]
        day_week_after = self.get_rang_week(num_week - 1)[0]
        num_week_after = self.dif_date(-1, day_week_after['date_final']).isocalendar()[1]
        wn = WeekNumber.objects.filter(num_week=num_week_after)
        if num_week_after != num_week or not wn.exists():
            print('this num_week not exists.')
            value_week_before = 0
            value_invest_before = 0
        else:
            wn = wn.first()
            value_week_before = wn.value_week
            value_invest_before = wn.value_invest
        week_before = []
        week_before.append({
                            'value_week_before': value_week_before,
                            'value_invest_before': value_invest_before
        })

        return week_before

    def get_rang_week(self, num_week):
        """
        :param num_week:
        :return:
        """
        _now_week = this_week()
        dif_day = ( _now_week - num_week ) * 7 + datetime.today().weekday()
        day = self.dif_date(dif_day)
        day_week = []
        day_week.append({
                        'date_init' : day,
                        'date_final' : self.dif_date(-6, day)
        })
        return day_week

    def get_gap_week(self, _date_init):
        """
        :param _date_init:
        :return:  all days in the week
        """
        week = []
        day_week = 0
        while day_week < 7:
            week.append(self.dif_date(-day_week, _date_init))
            day_week += 1
        return week

    def dif_date(self, day, date=None):
        """
        :param day:
        :param date:
        :return:
        """
        if date is None: date = datetime.today().date()
        day = date.toordinal() - day
        return date.fromordinal(day)

    def get_value_week(self, week):
        """
        :param week:
        :return:
        """
        extracts = Extract.objects.filter(
                                            date_purchase__range=[week['date_init'], week['date_final']]
                                            #, provider__type_launch__investment=False
                                            #, provider__type_launch__cost_fixo=False
                                        )
        tot_debit = 0
        tot_credit = 0
        value_debit_week = 0
        value_transf_deb = 0
        value_transf_cre = 0
        value_week = []
        for extract in extracts:
            tot_debit += extract.value_debit
            tot_credit += extract.value_credit
            if not extract.provider.type_launch.cost_fixo and not extract.provider.type_launch.investment:
                value_debit_week += extract.value_debit
            if extract.provider.type_launch.investment:
                value_transf_cre += extract.value_credit
                value_transf_deb += extract.value_debit
        value_transf = value_transf_deb - value_transf_cre
        week_before = self.get_value_week_before(week['date_init'])[0]
        total_week = week_before['value_week_before'] - tot_debit + tot_credit
        value_week.append({
                            'value_debit_week': value_debit_week,
                            'value_credit_week': tot_credit,
                            'value_week': total_week,
                            'value_transf': value_transf,
                            'value_invest_before': week_before['value_invest_before'],
                            'value_week_before': week_before['value_week_before']
        })
        return value_week