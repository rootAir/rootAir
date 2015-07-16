# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0036_delete_investment'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeknumber',
            name='percent_result',
            field=models.CharField(blank=True, max_length=1),
            preserve_default=True,
        ),
    ]
