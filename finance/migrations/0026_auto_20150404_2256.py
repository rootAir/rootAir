# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0025_auto_20150404_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='result',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
