# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0055_auto_20150515_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeknumber',
            name='available_broker',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
