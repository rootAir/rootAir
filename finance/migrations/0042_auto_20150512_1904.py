# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0041_auto_20150512_1902'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extract',
            options={'managed': False},
        ),
    ]
