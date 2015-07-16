# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0026_auto_20150404_2256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weeknumber',
            old_name='value_prevision',
            new_name='value_trade',
        ),
    ]
