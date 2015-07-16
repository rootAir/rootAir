# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0017_auto_20150223_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extract',
            name='provider',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='provider',
            name='num_week',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='provider',
            name='type_launch',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
