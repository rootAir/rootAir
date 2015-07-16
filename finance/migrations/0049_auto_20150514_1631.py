# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0048_auto_20150514_0855'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weeknumber',
            options={'managed': False},
        ),
    ]
