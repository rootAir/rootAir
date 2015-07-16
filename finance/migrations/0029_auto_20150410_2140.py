# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0028_typelaunch_investment'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeknumber',
            name='quant_trade',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weeknumber',
            name='tax_trade',
            field=models.DecimalField(max_digits=8, default=0, decimal_places=2),
            preserve_default=False,
        ),
    ]
