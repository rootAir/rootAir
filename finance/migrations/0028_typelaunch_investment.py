# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0027_auto_20150405_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='typelaunch',
            name='investment',
            field=models.BooleanField(db_index=True, default=False),
            preserve_default=True,
        ),
    ]
