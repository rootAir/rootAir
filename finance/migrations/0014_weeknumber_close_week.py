# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0013_investment'),
    ]

    operations = [
        migrations.AddField(
            model_name='weeknumber',
            name='close_week',
            field=models.BooleanField(db_index=True, default=False),
            preserve_default=True,
        ),
    ]
