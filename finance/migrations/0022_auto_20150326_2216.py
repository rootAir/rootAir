# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0021_auto_20150326_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extract',
            name='provider',
            field=models.ForeignKey(to='finance.Provider', blank=True, null=True),
            preserve_default=True,
        ),
    ]
