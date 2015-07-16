# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_auto_20141226_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='calendar',
            field=models.CharField(max_length=50),
            #preserve_default=True,
        ),
    ]
