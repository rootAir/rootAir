#!/usr/bin/env python
import os
import sys
# import pika

# from tasks import *

if __name__ == "__main__":

    from django.core.management import execute_from_command_line
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

    # import django
    # django.setup()

    execute_from_command_line(sys.argv)


