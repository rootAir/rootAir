# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0051_auto_20150515_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='provider',
            name='observation',
            field=models.TextField(null=True, blank=True),
        ),
    ]
