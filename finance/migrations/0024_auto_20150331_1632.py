# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0023_weeknumber_value_cost_week'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weeknumber',
            old_name='value_cost_week',
            new_name='value_credit_week',
        ),
        migrations.AddField(
            model_name='weeknumber',
            name='value_debit_week',
            field=models.DecimalField(max_digits=8, default=0, decimal_places=2),
            preserve_default=False,
        ),
    ]
