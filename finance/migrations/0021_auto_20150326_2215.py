# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0020_auto_20150318_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='num_week',
            field=models.ForeignKey(null=True, to='finance.WeekNumber', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='provider',
            name='type_launch',
            field=models.ForeignKey(null=True, to='finance.TypeLaunch', blank=True),
            preserve_default=True,
        ),
    ]
