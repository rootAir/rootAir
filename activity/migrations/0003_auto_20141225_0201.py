# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0002_auto_20141225_0153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='typeactivity',
            old_name='have_cost',
            new_name='positive',
        ),
    ]
