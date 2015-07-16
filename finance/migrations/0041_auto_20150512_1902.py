# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0040_auto_20150512_1900'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extract',
            options={'managed': True},
        ),
    ]
