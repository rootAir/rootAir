# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0024_auto_20150331_1632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provider',
            name='num_week',
        ),
        migrations.AddField(
            model_name='investment',
            name='gain',
            field=models.DecimalField(decimal_places=2, max_digits=8, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='investment',
            name='result',
            field=models.DecimalField(decimal_places=2, max_digits=8, default=0),
            preserve_default=False,
        ),
    ]
