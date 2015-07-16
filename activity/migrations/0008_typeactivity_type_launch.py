# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0027_auto_20150405_0854'),
        ('activity', '0007_auto_20150331_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='typeactivity',
            name='type_launch',
            field=models.ForeignKey(blank=True, null=True, to='finance.TypeLaunch'),
            preserve_default=True,
        ),
    ]
