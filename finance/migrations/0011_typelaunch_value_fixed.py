# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0010_weeknumber_value_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='typelaunch',
            name='value_fixed',
            field=models.DecimalField(decimal_places=2, max_digits=8, default=0),
            preserve_default=False,
        ),
    ]
