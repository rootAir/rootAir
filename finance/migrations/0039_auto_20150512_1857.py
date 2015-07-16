# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0038_auto_20150508_1700'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extract',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='provider',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='typelaunch',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='weeknumber',
            options={'managed': False},
        ),
    ]
