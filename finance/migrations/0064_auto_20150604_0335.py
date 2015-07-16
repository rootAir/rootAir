# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0063_auto_20150604_0309'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weeknumber',
            options={'managed': True},
        ),
    ]
