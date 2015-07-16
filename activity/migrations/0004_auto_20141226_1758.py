# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0003_auto_20141225_0201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='hour_final',
            field=models.DateTimeField(null=True, verbose_name='hour final'),
            #preserve_default=True,
        ),
        migrations.AlterField(
            model_name='activity',
            name='hour_init',
            field=models.DateTimeField(null=True, verbose_name='hour init'),
            #preserve_default=True,
        ),
    ]
