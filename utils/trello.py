#!/usr/bin/python
from datetime import datetime
from django.conf import settings
from utils.util import *
from requests_oauthlib import OAuth1Session

# from trello import TrelloClient
from build.pytrello.trello import *
from build.pytrello.trello.util import *
import os


def client_trello(_token = settings.TRELLO_TOKEN, _token_secret = settings.TRELLO_TOKEN_SECRET):
    """
    :param _token:
    :param _token_secret:
    :return:
    """
    try:
        _trello = TrelloClient(
                        api_key = settings.TRELLO_API_KEY,
                        api_secret = settings.TRELLO_API_SECRET,
                        token = _token,
                        token_secret = _token_secret
        )
        return _trello
    except:
        create_oauth_token(
                                expiration=None,
                                scope=None,
                                key= settings.TRELLO_API_KEY,
                                secret= settings.TRELLO_API_SECRET,
                                name=None,
                                output=True
        )
        _token = None
        _token_secret = None
        return client_trello(_token, _token_secret)

def get_list_cards(_name_list):
    """
    :param name_list:
    :return:
    """
    _board = get_board_trello()
    list_id = get_list_id(_board, _name_list)
    _list = List(_board, list_id)
    return _list

def get_name_list(_date):
    """
    :param date:
    :return:
    """
    return DayL[_date.weekday()] + "_" + str("%02d" % (_date.day,))

def get_board_trello(day=None):
    """
    :param day:
    :return:
    """
    if day is None:
        day = datetime.today().date()
    board_id = get_board_id( Month.get(day.month) )
    _trello = client_trello()
    _board = Board(_trello, board_id)
    if day.month < datetime.today().month:
        _board.close()
    return _board

def get_board_id(_name_board):
    """
    :param _name_board:
    :return:
    """
    _trello = client_trello()
    boards = _trello.list_boards()
    board_id = None
    for _board in boards:
        if str(_board.name, "utf-8").upper() == _name_board.upper():
            board_id = _board.id

    if board_id is None:
        board_id = _trello.add_board(_name_board).id
    return board_id

def get_list_id(board, name_list):
    """
    :param board:
    :param name_list:
    :return:
    """
    lists = board.all_lists()
    list_id = None
    for _list in lists:
        if str(_list.name, "utf-8").upper() == name_list.upper():
            list_id = _list.id

    if list_id is None:
        list_id = board.add_list(name_list).id
    return list_id
