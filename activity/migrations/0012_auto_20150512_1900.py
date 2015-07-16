# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0011_auto_20150512_1857'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='activity',
            table='activity_activity',
        ),
        migrations.AlterModelTable(
            name='planned',
            table='activity_planned',
        ),
        migrations.AlterModelTable(
            name='typeactivity',
            table='activity_typeactivity',
        ),
    ]
