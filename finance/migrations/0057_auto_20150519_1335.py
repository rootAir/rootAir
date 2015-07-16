# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0056_weeknumber_available_broker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeknumber',
            name='available_broker',
            field=models.DecimalField(blank=True, decimal_places=2, null=True, max_digits=8),
        ),
    ]
