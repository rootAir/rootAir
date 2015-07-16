#!/usr/bin/python
# # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.conf import settings
from oauth2client.client import SignedJwtAssertionCredentials
import httplib2
import pprint
import json
import gspread

# import PyOpenSSL
# json_key = json.load(open('utils/gspread-report-week.json'))

class Credentials (object):
    def __init__ (self, access_token=None):
        self.access_token = access_token

    def refresh (self, http):
        """
        :param http:
        :return:
        """
        # get new access_token
        # this only gets called if access_token is None

def get_worksheet(num_week, month=None):
	"""
	:param num_week:
	:param month:
	:return:
	"""
	scope = ['https://spreadsheets.google.com/feeds']
	credentials = SignedJwtAssertionCredentials(
                                                    settings.GOOGLE_JSON_KEY['client_email'],
                                                    bytes(settings.GOOGLE_JSON_KEY['private_key'], 'utf-8'),
                                                    scope
    )
	gc = gspread.authorize(credentials)
	sh = gc.open_by_key(settings.DOC_KEY_GOOGLE)

	if not month is None:
		name_worksheet = 'result ' + month
	else:
		name_worksheet = 'week ' + str(num_week)
	rows = "100"
	cols = "30"
	try:
		worksheet = sh.add_worksheet(title=name_worksheet, rows=rows, cols=cols)
	except Exception:
		worksheet = sh.worksheet(name_worksheet)
		clean_worksheet(worksheet)
	return worksheet

def clean_worksheet(worksheet):
	"""
	:param worksheet:
	:return:
	"""
	w_data = worksheet.get_all_values()
	if w_data.__len__() != 0:
		range_init = get_addr_int(1,1)
		_range = get_range(w_data)
		cell_list = worksheet.range(_range)
		for cell in cell_list:
			cell.value = ''
		worksheet.update_cells(cell_list)

def get_range(matriz):
	"""
	:param matriz:
	:return:
	"""
	range_init = get_addr_int(1, 1)
	line_final = len(matriz)
	coll_final = len(matriz[0])
	range_final = get_addr_int(line_final, coll_final)
	_range = range_init + ":" + range_final
	return _range

def send_week(worksheet, _range, matriz):
	"""
	:param worksheet:
	:param _range:
	:param matriz:
	:return:
	"""
	cell_list = worksheet.range(_range)
	i = 0
	for row in matriz:
		for coll in row:
			cell_list[i].value = str(coll)
			i += 1
	worksheet.update_cells(cell_list)

def get_addr_int(row, col):
	"""Translates cell's tuple of integers to a cell label.
	The result is a string containing the cell's coordinates in label form.
	:param row: The row of the cell to be converted.     Rows start at index 1.
	:param col: The column of the cell to be converted.  Columns start at index 1.
	Example:   >>> wks.get_addr_int(1, 1)    A1
	"""
	_MAGIC_NUMBER = 64
	row = int(row)
	col = int(col)
	if row < 1 or col < 1:
		raise IncorrectCellLabel('(%s, %s)' % (row, col))
	div = col
	column_label = ''
	while div:
		(div, mod) = divmod(div, 26)
		if mod == 0:
			mod = 26
			div -= 1
		column_label = chr(mod + _MAGIC_NUMBER) + column_label

	label = '%s%s' % (column_label, row)
	return label
