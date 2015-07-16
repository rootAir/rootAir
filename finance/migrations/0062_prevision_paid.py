# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0061_auto_20150530_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='prevision',
            name='paid',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
