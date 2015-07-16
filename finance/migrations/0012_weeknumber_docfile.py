# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0011_typelaunch_value_fixed'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeknumber',
            name='docfile',
            field=models.FileField(default=datetime.datetime(2015, 2, 8, 16, 45, 34, 589035, tzinfo=utc), upload_to='documents/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
