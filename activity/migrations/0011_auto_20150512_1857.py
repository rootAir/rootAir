# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_planned'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='planned',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='typeactivity',
            options={'managed': False},
        ),
    ]
