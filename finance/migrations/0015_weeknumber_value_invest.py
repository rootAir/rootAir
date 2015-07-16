# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0014_weeknumber_close_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeknumber',
            name='value_invest',
            field=models.DecimalField(max_digits=8, default=0, decimal_places=2),
            preserve_default=False,
        ),
    ]
