# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0060_auto_20150530_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prevision',
            name='date_payment',
            field=models.DateField(null=True, blank=True, verbose_name='date payment'),
        ),
    ]
