from kombu import Queue, Exchange

###########################################################
# Celery-RabbitMQ for Linux
BROKER_HOST = "dsfasfd"
BROKER_PORT = 5672
BROKER_VHOST = "rootair"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
RABBIT_URL = "amqp://qwr:guest@lll:5672"
# CELERY_ENABLE_UTC = True
# CELERY_TIMEZONE = "America/Sao_Paulo"


CELERY_QUEUES = (
     Queue('default', Exchange('default'), routing_key='default'),
     Queue('celery', Exchange('celery'), routing_key='celery'),
)


# CELERY_DEFAULT_QUEUE = "celery"
# CELERY_DEFAULT_EXCHANGE_TYPE = "fanout"
# CELERY_DEFAULT_ROUTING_KEY = "default"

##########################################################
# Celery
# RabitQM Broker configuration for Celery
# http://ask.github.com/celery/getting-started/first-steps-with-django.html

CELERY_IMPORTS = (
                    "finance.tasks",
)


CELERY_SEND_TASK_ERROR_EMAILS = True
CELERYD_PREFETCH_MULTIPLIER = 1
CELERYD_MAX_TASKS_PER_CHILD = 1


# Task hard time limit in seconds. The worker processing the task
# will be killed and replaced with a new one when this is exceeded.
# 86400 = 24 hours
CELERYD_TASK_TIME_LIMIT = 2 #86400

# CELERYD_USER = "zinauser"
# CELERYD_GROUP = "www"

# CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
# CELERYBEAT_LOG_FILE = '/var/log/celery/%n-beat.log'
# CELERYBEAT_PID_FILE = '/var/run/celery/%n-beat.pid'
# CELERYBEAT_SCHEDULE = None

CELERYD_USER = "guest"
CELERYD_GROUP = "guest"

##########################################################
# Celery Queue
CELERY_QUEUE_SYNC_DB = 'sync_db'
CELERY_QUEUE_ADD = 'add'


###############################################################################
# Celery
# import djcelery
# djcelery.setup_loader()


# ## Using the database to store results
# CELERY_RESULT_BACKEND = "database"
# CELERY_RESULT_DBURI = "sqlite:///celerydb.sqlite"
#
# Results published as messages (requires AMQP).
# CELERY_RESULT_BACKEND = 'amqp://'

#
# CELERY_TASK_RESULT_EXPIRES = 18000  # 5 hours.
#
#
# Using multiple memcached servers:
# CELERY_RESULT_BACKEND = """
#     cache+memcached://172.19.26.240:11211;172.19.26.242:11211/
# """.strip()
#
# CELERY_CACHE_BACKEND_OPTIONS = {'binary': True,
#                                 'behaviors': {'tcp_nodelay': True}}
#
# CELERY_RESULT_ENGINE_OPTIONS = {'echo': True}
#
# config file for Celery Daemon
