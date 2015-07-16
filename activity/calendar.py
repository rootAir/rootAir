# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from utils.util import *
from django.db import models
from datetime import datetime
from django.contrib.contenttypes.models import *
from django.db.models import Sum, Max
from django.contrib import messages
from django.db import transaction
from django.conf import settings
import xlrd, os, time

class Calendar(models.Model):

	def get_description(card):
		"""
		:param card:
		:return:
		"""
		teste = card
		try:
			desc = card[0].split(':')[1].strip()
		except Exception:
			print(teste)
		return desc

	def get_cards_calendar(self, _list):
		"""
		:param _list:
		:return:
		"""
		num_card = _list.__len__()
		cards = [['' for coll in range(0)] for row in range(num_card)]
		line = 0
		for card in _list:
			card = str(card.name, "utf-8").split("_")
			if card.__len__() > 1:
				cards[line].append(get_description(card))
				cards[line].append(get_date_activity(card))
				cards[line].append(get_hour_init(card))
				cards[line].append(get_hour_final(card))
				cards[line].append(get_calendar(card))
				cards[line].append(get_type_activity(card))
				line += 1

			card = str(card.name, "utf-8").split("-")
		return cards

	def get_date_activity(card):
		"""
		:param card:
		:return:
		"""
		if card.__len__() == 3 or card.__len__() == 2:
			date = card[1].split()
			day = format(int(date[1]),'02')
			mounth = format(int(MesL.index(date[2])), '02')
			if card.__len__() == 3 and card[2].split().__len__() == 6:
				year = card[2].split()[3]
			else:
				year = date[3]
			date = str(day) + '-' + str(mounth) + '-' + str(year)
		#date = datetime.strptime(date, '%d-%m-%Y').date()
		return date

	def get_hour_init(card):
		"""
		:param card:
		:return:
		"""
		_hour = card[1].split()
		if card.__len__() == 2:
			hour = _hour[4]
		else:
			if _hour.__len__() == 5:
				hour = _hour[4]
			else:
				hour = _hour[3]
		#hour = datetime.strptime(hour, '%H:%M')
		return hour

	def get_hour_final(card):
		"""
		:param card:
		:return:
		"""
		if card.__len__() == 2:
			hour = '00:00'
		if card.__len__() == 3:
			if card[2].split().__len__() == 6:
				hour = card[2].split()[4]
			else:
				hour = card[2].split()[0]
		#hour = datetime.strptime(hour, '%H:%M')
		return hour

	def get_calendar(card):
		"""
		:param card:
		:return:
		"""
		if card.__len__() == 2:
			type_name = card[1].split()[5]
		else:
			if card[2].split().__len__() == 6:
				type_name = card[2].split()[5]
			else:
				type_name = card[2].split()[1]
		type_name = type_name[1:][:-1]
		return type_name

	def get_time_total(card):
		"""
		:param card:
		:return:
		"""
		time_total = 0  #calc after saver
		return time_total

	def get_type_activity(card):
		"""
		:param card:
		:return:
		"""
		# type_name = type_name.split()[1]
		# return type_name[1:][:-1]
		type_activity = None
		return type_activity

	def get_list_id(board, name):
		"""
		:param board:
		:param name:
		:return:
		"""
		lists = board.all_lists()
		for _list in lists:
			if str(_list.name, "utf-8") == name:
				list_id = _list.id
		if list_id is None: print('list activity not fount')
		return list_id
