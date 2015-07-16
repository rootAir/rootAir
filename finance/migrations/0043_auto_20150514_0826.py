# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0042_auto_20150512_1904'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weeknumber',
            options={'managed': True},
        ),
    ]
