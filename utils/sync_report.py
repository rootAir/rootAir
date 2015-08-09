# -*- coding: utf-8 -*-
#!/usr/bin/env python
from utils.util import *
from finance.week_number import WeekNumber
from finance.extract import Extract
from finance.type_launch import TypeLaunch
from broker.investment import Investment
from activity.activity import Activity
from activity.planned import Planned
from django.conf import settings
# from utils.trello import *
from utils.worksheet import *
from utils.dropbox import *
from threading import Thread
from time import sleep
from datetime import timedelta
from datetime import datetime
from django.conf import settings
from django.db import transaction, connections
import time, sys, threading, inspect, os


# FilteredListView options.
search_fields = ['date_range', 'date', 'type']
filter_fields = ['is_active', 'is_staff', 'is_superuser']
default_order = 'data'


class SyncReport():

    def sync_report(self):
        """
        :return: init count 4 week to sync first month
        """
        _num_week = this_week()
        self.report_week()
        _week_init = _num_week - 4
        for num_week in range(_week_init, _num_week):
            num_week += 1
            self.report_week(num_week)
            print('Call sync report week = ' + str(num_week))

    def report_week(self, _num_week=None):
        """
        :param num_week:
        :return:
        """
        if _num_week is None: _num_week = this_week()
        wn = WeekNumber()
        ext = Extract()
        act = Activity()
        _pla = Planned()
        _week = wn.get_or_create(_num_week, True)
        gap_week = wn.get_gap_week(_week.date_init)

        import ipdb; ipdb.set_trace()
        if _num_week == this_week():
            _pla.get_tasks_week()
            wn.import_extract_itau()
            wn.import_extract_mycap()

        m_summary_ext = self.get_matrix(gap_week, _week, Extract.__name__, None)
        m_summary_activ = self.get_matrix(gap_week, _week, Activity.__name__, None)
        m_details_ext = self.get_matrix(gap_week, _week, None, Extract.__name__)
        m_details_activ = self.get_matrix(gap_week, _week, None, Activity.__name__)

        for day in gap_week:
            cost_week = ext.get_cost_week(m_details_ext, day)
            try:
                activ_week = act.report_activity(m_details_activ, day)
            except Exception:
                print("trello unauthorized permission requested.")
                pass
        #     activ_summary = act.report_group_activity(m_summary_activ, day, _week)
        #
        # type_launch = TypeLaunch.objects.filter().order_by('-cost_fixo')
        # tot_week_before = wn.get_value_week_before(_week.date_init)[0]
        # tot_week_before = tot_week_before['value_week_before']
        # summary = self.get_summary_week(_week, m_summary_ext, type_launch, tot_week_before)
        # matrix = self.join_matrix(summary, cost_week)
        # matrix = self.join_matrix(matrix, activ_summary)
        # #matrix = self.join_matrix(matrix, activ_week)
        # _invest = self.invest_week(_week)
        # matrix = self.join_matrix(matrix, _invest)

        # worksheet = get_worksheet(_num_week)
        # _range = get_range(matrix)
        # send_week(worksheet, _range, matrix)

    def get_matrix(self, gap_week, _week, _summary, _details):
        """
        :param gap_week:
        :param _week:
        :param _summary:
        :param _details:
        :return:
        """
        more_line = 0
        less_line = 1
        for day in gap_week:
            if _summary == 'Extract':
                less_line = self.summary_extract(_week)
            if _summary == 'Activity':
                less_line = self.summary_activity(_week)

            if _details == 'Extract':
                less_line = self.details_extract(day)
            if _details == 'Activity':
                less_line = self.details_activity(day)
            if less_line > more_line:
                more_line = less_line
        matrix_week = [['' for coll in range(0)] for row in range(more_line + 4)]
        return matrix_week

    def join_matrix(self, matr_1, matr_2):
        """
        :param matr_1:
        :param matr_2:
        :return: all line to inclusion coll
        """
        len_coll_m1 = matr_1[0].__len__()   # matrix with same amount column
        len_coll_m2 = matr_2[0].__len__()
        if len_coll_m1 > len_coll_m2:
            len_coll = len_coll_m1
        else:
            len_coll = len_coll_m2
        line = 0
        while line < len(matr_1):
            while len(matr_1[line]) < len_coll:
                matr_1[line].append('')
            line += 1
        line = 0
        while line < len(matr_2):
            while len(matr_2[line]) < len_coll:
                matr_2[line].append('')
            line += 1
        matr_1 += matr_2
        return matr_1

    def get_summary_week(self, _week, summary, tp_launch, tot_week_before):
        """
        :param _week:
        :param summary:
        :param tp_launch:
        :param tot_week_before:
        :return:
        """
        first_day = name_day(_week.date_init)
        last_day = name_day(_week.date_final)
        ext = Extract()
        act = Activity()
        value_week = ext.get_total_week(_week, _type=None)
        line = 0
        summary[line].append(first_day)
        summary[line].append("TO")
        summary[line].append(last_day)
        _today = datetime.today()
        summary[line].append("Account Itau day %s %s:%s" %(_today.day, str(_today.hour), str(_today.minute)))
        if value_week.__len__() > 1:
            line = 1
            value_debit = value_week[0]
            value_credit = value_week[1]
            total_week = value_week[2]
            # tot_week_before = value_week[3]
            total_week = tot_week_before - value_debit + value_credit
            if value_credit > value_debit:
                summary[line].append("Result Positive")
            else:
                summary[line].append("Result Negative")
            summary[line].append(str(value_debit).replace('.',','))
            summary[line].append(str(value_credit).replace('.',','))
            summary[line].append(str(total_week).replace('.',','))

            line = 2
            _local = 'local'
            if not settings.DATABASE_LOCAL: _local = 'heroku'
            summary[line].append("Cost Week")
            summary[line].append("Debit" + _local)
            summary[line].append("Credit")
            summary[line].append("Total")
            summary[line].append("Time")
            summary[line].append("Cost per time")
            summary[line].append("Recipe per time")

            line = 3
            for tp in tp_launch:
                tot_week_type = ext.get_total_week(_week, tp.id)
                if tot_week_type.__len__() > 1:
                    value_debit = str(tot_week_type[0]).replace('.',',')
                    value_credit = str(tot_week_type[1]).replace('.',',')
                    value_total = str(tot_week_type[2]).replace('.',',')
                    summary[line].append(tp.type_name)
                    summary[line].append(value_debit)
                    summary[line].append(value_credit)
                    summary[line].append(value_total)

                    time_cost = act.get_time_type_launch(_week, tp.id)
                    if time_cost is None:
                        time_cost = ''
                        cost_per_time = ''
                        receit_per_time = ''
                    else:
                        _cost_type = str_to_float(value_debit)
                        cost_per_time = round(_cost_type / float(time_cost), 2)
                        _receit_type = str_to_float(value_credit)
                        receit_per_time = round(_receit_type / float(time_cost), 2)

                        time_cost = str(time_cost).replace('.',',')
                        cost_per_time = str(cost_per_time).replace('.',',')
                        receit_per_time = str(receit_per_time).replace('.',',')
                    summary[line].append(time_cost)
                    summary[line].append(cost_per_time)
                    summary[line].append(receit_per_time)
                    line += 1
        return summary

    def summary_extract(self, _week):
        """
        :param _week:
        :return:
        """
        extracts = Extract.objects.filter(date_purchase__range=[_week.date_init, _week.date_final])
        less_line = extracts.values('provider__type_launch_id').distinct().count()
        return less_line

    def details_extract(self, day):
        """
        :param day:
        :return:
        """
        less_line = Extract.objects.filter(date_purchase=day).count()
        return less_line

    def summary_activity(self, _week):
        """
        :param _week:
        :return:
        """
        act = Activity.objects.filter(date_activity__range=[_week.date_init, _week.date_final])
        less_line = act.values('type_activity__type_name').distinct().count()
        return less_line

    def details_activity(self, day):
        """
        :param day:
        :return:
        """
        less_line = Activity.objects.filter(date_activity=day).count()
        return less_line

    def invest_week(self, _week):
        """
        :param _week:
        :return:
        """
        invest = Investment.objects.filter(opening__range=[_week.date_init, _week.date_final]).order_by('opening', 'time')
        _line = invest.count()
        matrix = [['' for coll in range(0)] for row in range(_line + 1)]

        line = 0
        matrix[line].append('Data')
        matrix[line].append('Ativo')
        matrix[line].append('Quant Compra')
        matrix[line].append('Preco Compra')
        matrix[line].append('Hora')
        matrix[line].append('Preco venda')
        matrix[line].append('Total compra')
        matrix[line].append('Total venda')
        matrix[line].append('Result %')
        matrix[line].append('lucro')

        tot_compra = 0
        for _ord in invest:
            line += 1
            result = 0
            matrix[line].append(_ord.opening)
            matrix[line].append(_ord.active)
            matrix[line].append(round(_ord.quant_execut))
            price_execut = str(_ord.price_execut).replace('.',',')
            if _ord.operation == "Compra":
                matrix[line].append(price_execut)
                val_compra = _ord.total
                val_venda = ''
                result = ''
                lucro = ''
            else:
                matrix[line].append('')

            matrix[line].append('')
            if _ord.operation == "Venda":
                matrix[line].append(price_execut)
                val_compra = ''
                val_venda = _ord.total
                result = _ord.result
                lucro = _ord.gain

            else:
                matrix[line].append('')

            matrix[line].append(str(val_compra).replace('.',','))
            matrix[line].append(str(val_venda).replace('.',','))
            matrix[line].append(str(result).replace('.',','))
            matrix[line].append(str(lucro).replace('.',','))

        return matrix

    def report_month(self, num_week):
        """
        :param num_week:
        :return:
        """
        month = month.get([datetime.today().month])
        type_launch = TypeLaunch.objects.filter().order_by('-cost_fixo')
        _line = type_launch.count()
        matrix = [['' for coll in range(0)] for row in range(_line + 1)]

        line = 0
        matrix[line].append('cost month %s' %month)
        line += 1
        for tl in type_launch:
            matrix[line].append(tl.type_name)
            line += 1

        line = 0
        matrix[line].append('prevision')
        line += 1
        for tl in type_launch:
            matrix[line].append(tl.value_fixed)
            line += 1

        line = 0
        matrix[line].append('fixo prevision')
        line += 1
        for tl in type_launch:
            if tl.cost_fixo:
                matrix[line].append(tl.value_fixed)
            else:
                matrix[line].append('')
            line += 1

        dif_week = 3  #4 week report_month
        wn = WeekNumber()
        ext = Extract()
        while dif_week >= 0:
            _num_week = (num_week - dif_week)
            _week = wn.get_or_create(_num_week)
            matrix = ext.get_cost_month(matrix, _week, type_launch)
            dif_week -= 1

        worksheet = get_worksheet(num_week, month)
        _range = get_range(matrix)
        send_week(worksheet, _range, matrix)


