# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0037_weeknumber_percent_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeknumber',
            name='percent_result',
            field=models.CharField(max_length=8, blank=True),
            preserve_default=True,
        ),
    ]
