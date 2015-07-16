# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0013_auto_20150516_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeactivity',
            name='type_desc',
            field=models.CharField(max_length=50),
        ),
    ]
