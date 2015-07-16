# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0018_auto_20150315_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='active',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
