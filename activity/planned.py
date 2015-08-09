from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import *
import os
from django.conf import settings
from utils.util import *
from django.db import transaction
from activity.type_activity import TypeActivity
from finance.type_launch import TypeLaunch
from django.db.models import Sum, Max
# from utils.trello import *
from datetime import datetime
from finance.week_number import *


class Planned(models.Model):
    # id = models.IntegerField(primary_key=True)  # AutoField?
    description = models.CharField(max_length=500, unique=False)
    date_activity = models.DateField('date activity')
    hour_init = models.DateTimeField('hour init', null=True, blank=True)   #datetime.datetime.now().strftime('%H:%M:%S')
    hour_final = models.DateTimeField('hour final', null=True, blank=True)
    num_week = models.IntegerField(null=True, blank=True)
    time_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    type_activity = models.ForeignKey(TypeActivity, blank=True, null=True)
    checked = models.BooleanField(default=False, db_index=True)
    state = models.CharField(max_length=20, unique=False)
    check_list = models.CharField(max_length=50, unique=False)
    synchronized = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True, null=True)

    class Meta:
        """
        """
        managed = True
        db_table = 'activity_planned'

    def save_json(self, _json):
        """
        :param _json:
        :return:
        """
        for _list in _json:
            _model = self._exists(_list)
            for field in _list:
                if not field in ['id', '_state', 'hour_init', 'hour_final']:
                    _model.__dict__[field] = _list[field]
            _model.save()

    def _exists(self, _list):
        """
        :param _list:
        :return:
        """
        if self.__class__.objects.filter(description=_list['description']).exists():
            return self.__class__.objects.get(description=_list['description'])
        else:
            return self.__class__()

    def get_tasks_week(self, _week= None):
        """
        :param _week:
        :return:  _card: get collection checklists this card week before
        """
        if _week is None:
            _week = WeekNumber().get_or_create()
        _num_week = _week.num_week
        _card_checklist_trello = self.get_card_checklist_trello(_num_week)

        if _num_week == this_week():
            _date_init = _week.date_init
            _date_final = _week.date_final
            _checklists = Planned.objects.filter(
                                        date_activity__range=[_week.date_init, _week.date_final],
                                        checked=False
            ).order_by('check_list')

            for _checklist in _checklists.values('check_list').distinct():
                _checklist_items = []
                _checklist_name = _checklist['check_list']
                for _item in _checklists.filter(checklist= _checklist_name):
                    _checklist_items.append({
                                                'name': _item['description'],
                                                'checked': False,
                                                'state': 'incomplete'
                    })
                _card_checklist_trello.add_checklist(_checklist_name, _checklist_items)

    def get_card_checklist_trello(self, _num_week= this_week(), _name_list_checklist= 'rootair'):
        """
        :param _num_week:
        :param _name_list_checklist:
        :return:
        """
        _list_cards_checklist = get_list_cards(_name_list_checklist)
        _name_card_checklist = 'W%s' %str(_num_week)
        for _card_checklist in _list_cards_checklist.list_cards():
            _card_name = str(_card_checklist.name, "utf-8").upper()
            if _card_name == _name_card_checklist:
                return _card_checklist
            else:
                _card_checklist.fetch()
                _checklists = _card_checklist.fetch_checklists()
                self.save_checklist_trello(_checklists)
                _card_checklist.set_closed(True)

        _card_checklist = _list_cards_checklist.add_card(_name_card_checklist)
        return _card_checklist

    def save_checklist_trello(self, _checklists):
        """
        :param _checklists:
        :return:
        """
        _ck_card_week_trello = []
        for _checklist in _checklists:
            _checklist_name = _checklist.name.strip()
            for _item in _checklist.items:
                _ck_card_week_trello.append({
                                                'description': _item['name'].strip(),
                                                'date_activity': datetime.today().date(),
                                                # 'hour_init': '',
                                                # 'hour_final': '',
                                                'time_total': 0,
                                                'type_activity': '',
                                                'checked': _item['checked'],
                                                'state': _item['state'],
                                                'check_list': _checklist_name,
                                                'synchronized': 'L',
                })
        self.save_json(_ck_card_week_trello)