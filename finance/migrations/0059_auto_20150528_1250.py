# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0058_auto_20150528_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeknumber',
            name='date_closed',
            field=models.DateTimeField(null=True, verbose_name='time closed week', blank=True),
        ),
    ]
