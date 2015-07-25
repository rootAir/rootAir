# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from datetime import timedelta
from threading import Thread
from time import sleep
from django.db import transaction, connections
from utils.util import *
from django.db.models import Sum, Max
from django.contrib import messages
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from broker.trade_sell import Trade
from broker.trade_active import TradeActive
from broker.wallet_buy import *
from utils.webselenium import *
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.select import Select
from finance.week_number import WeekNumber
import time, sys, threading, inspect, os


__author__ = 'RootAir'
os.environ["webdriver.chrome.driver"] = settings.CHROME_DRIVER

class SyncItau(threading.Thread):
    """Thread that executes a task every N seconds"""

    def __init__(self):
        """
        :return:
        """
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = 60
        self._robot_itau = RobotItau()

    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval

    def shutdown(self):
        """Stop this thread"""
        self._finished.set()

    def run(self):
        """
        :return: sleep for interval or until shutdown
        if self._finished.isSet(): return
        """
        while True:
            # import ipdb; ipdb.set_trace()
            self._finished.wait(self._interval)
            remove_files_path('*.txt')
            if self._robot_itau.export_extract_itau(self._robot_itau.driver):
                self._finished.wait(3)
                _week = WeekNumber()
                _week.send_file_to_dropbox()

    def __hash__(self):
        """
        :return:
        """
        return 0


class RobotItau(RobotRemoteChrome):
    _user_conta = settings.ITAU_CONTA
    _user_agencia = settings.ITAU_AGENCIA
    driver = None

    def __init__(self, work_package=None, debug=False, proxy=False, *args, **kwargs):
        """
        :param work_package:
        :param debug:
        :param proxy:
        :param args:
        :param kwargs:
        :return:
        """
        super(RobotItau, self).__init__(*args, **kwargs)
        self.debug = debug
        self.goto_url()

    def is_logged(self):
        """
        Check if user name is on html content
        """
        return settings.MYCAP_USERNAME in self.html_content

    def goto_order_details(self):
        """
        Go to HTML order detail
        """
        try:
            order_details_url = '?action=modifyOrderDetails&workPackageId=%s' % self.work_package.ipm_id
            self.driver.get(settings.IPM_DO_URL+order_details_url)
        except:
            self.driver.find_element_by_css_selector("#wpForm > table > tbody > tr > td > a").click()
        time.sleep(1)

    def do_login(self,password=None):
        """
        :param password:
        :return:
        """
        self.driver.find_element_by_id("campo_agencia").clear()
        self.driver.find_element_by_id("campo_agencia").send_keys(settings.ITAU_AGENCIA)
        self.driver.find_element_by_id("campo_conta").clear()
        self.driver.find_element_by_id("campo_conta").send_keys(settings.ITAU_CONTA)
        self.driver.find_element_by_class_name("btnSubmit").click()

    def goto_url(self):
        """
        :return:
        """
        self.driver.get("https://www.itau.com.br/")
        self.do_login(password=None)
        time.sleep(20)

    def export_extract_itau(self, _driver):
        """
        :param _driver:
        :return:
        """
        try:
            # self.html_content = self.driver.page_source
            # call_itau = 'javascript:KHRtoUni2C(\'WN3M10453MB M O3111\',' \
            #                                 '\'U20\',' \
            #                                 '\'JMIPJCDC6EPH\',' \
            #                                 '\'0F404D6C8E3F678A3B05635340A1521303E92A7528EC1C7EDF418FC4B2CB44A6C7C2028E6CA6C3F3E40EBD4A0C8257AA9477CBE9A9F4EC63761C853A7F5161D1\');'
            month = "%02d" % (datetime.today().month - 1)
            year = datetime.today().year
            _driver.find_element_by_id('Dia').clear()
            _driver.find_element_by_id('Dia').send_keys('01')
            _driver.find_element_by_id('Mes').clear()
            _driver.find_element_by_id('Mes').send_keys(str(month))
            _driver.find_element_by_id('Ano').clear()
            _driver.find_element_by_id('Ano').send_keys(str(year))
            # _driver.find_element_by_class_name('TRNinput').click()
            # _driver.execute_script(atalho)
            # _driver.find_element_by_class_name('lnkpadrao01')
            _driver.find_element_by_class_name('TRNinputBTN').click()
            # print('Generated extract itau month of - %s' %Month.get(datetime.today().month))
            return True
        except:
            # _driver.quit()
            return False