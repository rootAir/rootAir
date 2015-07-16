# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0017_auto_20150626_0546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='planned',
            options={'managed': True},
        ),
        migrations.AddField(
            model_name='planned',
            name='num_week',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
