import time, sys, threading, inspect, os
from threading import Thread
from time import sleep
from datetime import timedelta
from datetime import datetime
from django.conf import settings
from django.db import transaction, connections

# TaskThread
class SyncDb(threading.Thread):
    """Thread that executes a task every N seconds"""

    def __init__(self):
        threading.Thread.__init__(self)
        self._finished = threading.Event()
        self._interval = 1

    def setInterval(self, interval):
        """Set the number of seconds we sleep between executing our task"""
        self._interval = interval

    def shutdown(self):
        """Stop this thread"""
        self._finished.set()

    def run(self):
        while True:
            # if self._finished.isSet(): return
            if settings.DATABASE_LOCAL:
                self.sync_db()
            """sleep for interval or until shutdown"""
            # self._finished.wait(self._interval)

    def __hash__(self):
        #pass
        return 0

    def sync_db(self):
        """The task done by this thread - override in subclasses"""
        start_time = time.time()
        _class = self.get_all_class_app()
        for cls in _class:
            self.sinc_class(cls[1])
            self.update_sequence(cls[1])
        _time = timedelta(seconds=time.time() - start_time)
        print('=> Sincronized base in %s' %_time)

    def update_sequence(self, _class):
        cursor = connections[settings.DATABASE_REMOTE].cursor()
        _table = (_class.objects.model.__module__).replace('_','').replace('.','_')
        _query = 'SELECT pg_catalog.setval(pg_get_serial_sequence(\'%s\', \'id\'), MAX(id)) FROM %s;' %(_table, _table)
        cursor.execute(_query)

    #@transaction.non_atomic_requests(using=settings.DATABASE_REMOTE)
    # @transaction.commit_on_success(using='heroku')
    def sinc_class(self, _class):
        try:
            start_time = time.time()
            ds_local = _class.objects.all()
            ds = _class()
            for loc in ds_local:
                ds_remoto = _class.objects.using(settings.DATABASE_REMOTE).filter(id=loc.__dict__['id'])
                if not ds_remoto.exists() or loc.__dict__['synchronized'] != 'S':
                    for field in loc.__dict__:
                        if field != '_state':
                            ds.__dict__[field] = loc.__dict__[field]

                    ds.__dict__['synchronized'] = 'S'
                    ds.save(using=settings.DATABASE_REMOTE, force_insert=True)
                    ds.save()

            _time = timedelta(seconds=time.time() - start_time)
            print('Sincronized %s execution in %s'%(str(ds),_time))
            sys.stdout.flush()
        except:
            # transaction.rollback()
            # print('=> erro na synchronized sinc_class')
            pass
        # else:
        #     transaction.commit()

    def get_all_class_app(self):
        _apps = [
                    'finance.extract', 'finance.provider', 'finance.type_launch', 'finance.week_number',
                    'activity.activity', 'activity.type_activity',
                    'travel.place', 'travel.chain',
                    'broker.investment', 'broker.trade'
                ]
        from activity.activity import Activity
        from activity.type_activity import TypeActivity
        from finance.extract import Extract
        from broker.investment import Investment
        from finance.provider import Provider
        from finance.type_launch import TypeLaunch
        from finance.week_number import WeekNumber
        from travel.place import Place
        from travel.chain import Chain
        _class = []
        for _app in _apps:
            #__name__ = eval(_app)
            clsmembers = inspect.getmembers(sys.modules[_app], inspect.isclass)
            for cls in clsmembers:
                _class_model = cls[1]
                if _class_model.__module__ in _apps:
                    _class.append(cls)

        return _class

    def _sinc_database(self, table):
        extracts = Extract.objects.all()
        cont_line = extracts.__len__() + 5
        matrix = [['' for coll in range(0)] for row in range(cont_line)]
        line = 0
        matrix[line].append('test')

        worksheet = get_worksheet(table)
        _range = get_range(matrix)
        send_week(worksheet, _range, matrix)