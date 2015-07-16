# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0057_auto_20150519_1335'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RobotItau',
        ),
        migrations.AddField(
            model_name='weeknumber',
            name='date_closed',
            field=models.DateTimeField(null=True, verbose_name='time closed week'),
        ),
    ]
