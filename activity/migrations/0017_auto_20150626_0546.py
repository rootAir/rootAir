# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0016_auto_20150614_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planned',
            name='synchronized',
            field=models.CharField(blank=True, null=True, choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')], max_length=1),
        ),
    ]
