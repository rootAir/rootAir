from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import *
import os
from django.conf import settings
from utils.util import *
from utils.trello import *
from django.db import transaction
from activity.type_activity import TypeActivity
from finance.type_launch import TypeLaunch
from django.db.models import Sum, Max


class Activity(models.Model):
    # id = models.IntegerField(primary_key=True)  # AutoField?
    description = models.CharField(max_length=500, unique=False)
    date_activity = models.DateField('date activity')
    hour_init = models.DateTimeField('hour init', null=True)   #datetime.datetime.now().strftime('%H:%M:%S')
    hour_final = models.DateTimeField('hour final', null=True)
    time_total = models.DecimalField(max_digits=8, decimal_places=2) # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    calendar = models.CharField(max_length=50, unique=False)
    type_activity = models.ForeignKey(TypeActivity, blank=True, null=True)
    synchronized = models.CharField(max_length=1, choices=STATUS_CHOICES)


    class Meta:
        managed = False
        db_table = 'activity_activity'

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

    def report_group_activity(self, matrix, date, _week=None):
        """
        :param matrix:
        :param date:
        :param _week:
        :return:
        """
        if not _week is None:
            activs = Activity.objects.filter(date_activity__range=[_week.date_init, _week.date_final])
            activs = activs.order_by('type_activity__positive')
        else:
            activs = Activity.objects.filter(date_activity=date)
        activs = activs.values('type_activity__type_desc').distinct()
        line = 0
        for act in activs:
            _type = act['type_activity__type_desc']
            matrix[line].append(_type)
            matrix[line].append(self.total_activity(date, _type))
            matrix[line].append('')
            line += 1

        while line < matrix.__len__():
            matrix[line].append('')
            matrix[line].append('')
            matrix[line].append('')
            line += 1
        return matrix

    def get_time_activity(self, _week, _type_group):
        """
        :param _week:
        :param _type_group:
        :return:
        """
        _activities = Activity.objects.filter(
                                        date_activity__range=[_week.date_init, _week.date_final],
                                        type_activity__group = _type_group
                                      ).aggregate(Sum('time_total'))
        return _activities['time_total__sum']


    def total_activity(self, date, _type):
        """
        :param date:
        :param _type:
        :return:
        """
        activs = Activity.objects.filter(date_activity=date, type_activity__type_desc=_type)
        total = 0
        for act in activs:
            total += act.time_total
        if total == 0:
            total = ''
        else:
            total = str(total).replace('.',',')
        return total

    # @transaction.commit_on_success
    def sync_activity(self, date):
        """
        :param matrix:
        :param date:
        :return:
        """
        try:
            if not Activity.objects.filter(date_activity=date).exists():
                _board = get_board_trello(date)
                list_id = get_list_id(_board, get_name_list(date))
                _list = List(_board, list_id)
                _list_cards = _list.list_cards()
                if date < datetime.today().date() and self.list_complet(date, _list_cards):
                    _list_trello = self.get_list_trello(_list_cards, date)
                    # self.send_type_activity(_list_trello)
                    if self.save_cards(_list_trello):
                        _list.close()
        except:
            print('erro function sync_activity')
            # transaction.rollback()
            # pass
        # else:
        #     transaction.commit()

    def get_list_trello(self, _list, date):
        """
        :param _list:
        :param date:
        :return:
        """
        list_trello = []
        n_card = 0
        _hour_full = True
        for card in _list:
            card = str(card.name, "utf-8").split("_")
            n_card += 1
            _hour = card[0].replace(',','.')
            if isfloat(_hour):
                _hour = float(_hour)
                if n_card == 1:
                    _hour_init = 0
                    _hour_final = _hour
                else:
                    _hour_init = _hour_final
                    _hour_final += _hour

                if ( _hour % 1 == 0 ):
                    if ( _hour_full ):
                        _minut_init = ':00'
                        _minut_final = ':00'
                    else:
                        _minut_init = ':30'
                        _minut_final = ':30'
                        _hour_full = False
                elif ( _hour_full ):
                    _minut_init = ':00'
                    _minut_final = ':30'
                    _hour_full = True
                else:
                    _minut_init = ':30'
                    _minut_final = ':00'
                # if card[1].strip()[-2] == ',':
                #     _hour_init =+ card[1].strip()[-3:]
                h_init = "%02d" % (_hour_init % 13) + _minut_init
                h_final = "%02d" % (_hour_final % 13) + _minut_final
                # print('temp total = ' + str(_hour) + ' hora init = ' + h_init + ' hora final = ' + h_final)
                list_trello.append({
                                    'description': card[1][4:],
                                    'date_activity': date,
                                    'hour_init': datetime.strptime(str(date) + 'T' + h_init + 'Z', '%Y-%m-%dT%H:%MZ'),
                                    'hour_final': datetime.strptime(str(date) + 'T' + h_final + 'Z', '%Y-%m-%dT%H:%MZ'),
                                    'time_total': _hour,
                                    'calendar': None,
                                    'type_activity': card[1].split()[0]
                                    })
        return list_trello

    def list_complet(self, date, _list):
        """
        :param date:
        :param _list:
        :return:
        """
        try:
            hour_day = 0
            for card in _list:
                card = str(card.name, "utf-8").split("_")
                hour_card = card[0].replace(',','.')
                if isfloat(hour_card):
                    hour_day += float(hour_card)
            if hour_day != 24:  #hour_day 24h
                print('board %s have %s hour' %(date, hour_day))
                return False
            else:
                return True
        except:
            print('danger the format card = ')

    @transaction.non_atomic_requests
    def save_cards(self, _list):
        """
        :param _list:
        :return:
        """
        try:
            for card in _list:
                act = Activity()
                act.description = card['description']
                act.date_activity = card['date_activity']
                act.hour_init = card['hour_init']
                act.hour_final = card['hour_final']
                act.time_total = card['time_total']
                act.calendar = '-' #card['calendar']
                act.type_activity_id = self.get_type_activity(card['type_activity'])
                # act.type_activity_id = TypeActivity.objects.get(type_name__iexact=card['type_activity']).id
                act.save()
        except:
            transaction.rollback()
            print('erro save_cards trello.')
            # pass
            return False
        else:
            transaction.commit()
        return True

    # @transaction.commit_on_success
    def get_type_activity(self, type_act):
        """
        :param type_act:
        :return:
        """
        try:
            tp_act = TypeActivity.objects.filter(type_name__iexact= type_act)
            # MyClass.objects.filter(name__icontains=my_parameter)
            if not tp_act.exists():
                _tp_act = TypeActivity()
                _tp_act.type_name = type_act
                _tp_act.type_desc = "-"
                _tp_act.group = "-"
                _tp_act.positive = False
                _tp_act.type_launch_id = TypeLaunch.objects.get(type_name='Activity').id
                _tp_act.save()
                tp_id = _tp_act.id
            else:
                tp_id = tp_act.first().id
        except:
            print('erro function get_type_activity')
            # transaction.rollback()
        # else:
        #     transaction.commit()
        return tp_id

    def get_time_type_launch(self, _week, tp_launch):
        """
        :param _week:
        :param tp_launch:
        :return:
        """
        _time = Activity.objects.filter(
                                            date_activity__range=[_week.date_init, _week.date_final],
                                            type_activity__type_launch_id=tp_launch
                                        ).aggregate(Sum('time_total'))
        return _time['time_total__sum']