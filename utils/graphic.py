# -*- coding: utf-8 -*-
#!/usr/bin/env python
from utils.util import *
from finance.week_number import WeekNumber
from finance.extract import Extract
from finance.type_launch import TypeLaunch
# from broker.investment import Investment
from activity.activity import Activity
from activity.type_activity import TypeActivity
from activity.planned import Planned
from django.conf import settings
# from utils.trello import *
from .worksheet import *
from .dropbox import *
from threading import Thread
from time import sleep
from datetime import timedelta, datetime
from django.conf import settings
from django.db import transaction, connections
import time, sys, threading, inspect, os
import datetime, random
from nvd3 import linePlusBarChart, pieChart, cumulativeLineChart

_cost_activity_week = 'finance/templates/graphic/cost_activity_week.html'
_time_activity_day = 'activity/templates/graphic/time_activity_day.html'

class Graphic(object):
    def __init__(self):
        """
        :return:
        """
        self._interval = 30
        self.sync_graphic()

    def sync_graphic(self):
        """
        :return: init count 4 week to sync first month
        """
        _num_week = this_week()
        _week_init = _num_week - 4
        for num_week in range(_week_init, _num_week):
            num_week += 1
            self.update_graphic(num_week)

    def update_graphic(self, _num_week=None):
        """
        :param num_week:
        :return:
        """
        if _num_week is None: _num_week = this_week()
        _act = Activity()
        _wn = WeekNumber()
        _week = _wn.get_or_create(_num_week, True)
        _plan = Planned().get_tasks_week(_week)
        gap_week = _wn.get_gap_week(_week.date_init)

        for day in gap_week:
            activ_week = _act.sync_activity(day)

    def graphic_view(_name_graphic):
        """
        :param _name_graphic: compare -> actual / forecast
        :return:
        """
        os.system('python -m webbrowser -t \"http://localhost:63342/balance/%s\"' %_name_graphic)
        os.system('say bad results in week %s' %this_week()) # great good

    def graphic_cost_activity_week():
        """
        :return:
        """
        xdata = []
        ydata = []
        ydata2 = []
        output_file = open(_cost_activity_week, 'w')

        type = "Time activity"
        start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
        nb_element = 100
        _chart_activ = cumulativeLineChart(name=type, height=350, width=750, x_is_date=True)
        _chart_activ.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")
        xdata = list(range(nb_element))
        xdata = [start_time + x * 1000000000 for x in xdata]
        ydata = [i + random.randint(1, 10) for i in range(nb_element)]
        ydata2 = [x * 2 for x in ydata]
        extra_serie = {"tooltip": {"y_start": "", "y_end": " Calls"}}
        _chart_activ.add_serie(name="Count", y=ydata, x=xdata, extra=extra_serie)
        extra_serie = {"tooltip": {"y_start": "", "y_end": " Min"}}
        _chart_activ.add_serie(name="Duration", y=ydata2, x=xdata, extra=extra_serie)

        type = "Cost vs reserve week"
        _weeks = WeekNumber.objects.all().order_by('-date_init')
        for _num_week in range(0, this_week()):
            _time = int(time.mktime(_weeks[_num_week].date_final.timetuple()) * 1000)
            _credit = float(_weeks[_num_week].value_week + _weeks[_num_week].value_invest)
            _debit = float(_weeks[_num_week].value_debit_week + _weeks[_num_week].cost_fixed_week)
            xdata.append(_time)
            ydata.append(_debit)
            ydata2.append(_credit)
        _chart_cost = linePlusBarChart(
                                    name=type, height=350, width=750,
                                    x_is_date=True, x_axis_format="%d %b %Y",
                                    focus_enable=True
                                 )
        _chart_cost.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")
        kwargs = {}
        kwargs['bar'] = True
        extra_serie = {"tooltip": {"y_start": "$ ", "y_end": " week"}}
        _chart_cost.add_serie(name="Cost", y=ydata, x=xdata, extra=extra_serie, **kwargs)
        _chart_cost.add_serie(name="Reserve", y=ydata2, x=xdata, extra=extra_serie)

        _chart_activ.buildhtml()
        _chart_cost.buildcontent()

        output_file.write(_chart_activ.htmlcontent + _chart_cost.htmlcontent)
        output_file.close()
        graphic_view(_cost_activity_week)

    def graphic_time_activity_day():
        """
        :return:
        """
        output_file = open(_time_activity_day, 'w')
        _num_week = int(this_week()) - 1
        _week = WeekNumber.objects.get(num_week= _num_week)
        _act = Activity()
        _tp_acts = TypeActivity.objects.values('group').distinct()

        # xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
        # ydata = [3, 4, 0, 1, 5, 7, 3]
        xdata = []
        ydata = []
        _time = 0
        for _type_act in _tp_acts:
            _time_week = _act.get_time_activity(_week, _type_act['group'])
            if not _time_week is None and _time_week > 0:
                xdata.append(_type_act['group'])
                ydata.append(float(_time_week))
                _time += float(_time_week)

        type = 'Closed %s - time activity (%s hours weeks)' %(DayL[int(_time/24)-1], str(_time))
        chart = pieChart(name=type, color_category='category20c', height=450, width=450)
        chart.set_containerheader("\n\n<h2>" + type + "</h2>\n\n")

        extra_serie = {"tooltip": {"y_start": "", "y_end": " hs"}}
        chart.add_serie(y=ydata, x=xdata, extra=extra_serie)

        chart.buildhtml()
        output_file.write(chart.htmlcontent)
        output_file.close()
        # data = {
        #     'charttype': charttype,
        #     'chartdata': chartdata,
        # }
        # return render_to_response("graphic.html")
        # new_uri = '%s://%s%s%s' % (
        #         request.is_secure() and 'https' or 'http',
        #         site.domain,
        #         urlquote(request.path),
        #         (request.method == 'GET' and len(request.GET) > 0) and '?%s' % request.GET.urlencode() or ''
        #     ) http://eikke.com/django-domain-redirect-middleware/

        graphic_view(_time_activity_day)
