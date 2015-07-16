# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0062_prevision_paid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extract',
            options={'managed': True},
        ),
    ]
