# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0039_auto_20150512_1857'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='extract',
            table='finance_extract',
        ),
        migrations.AlterModelTable(
            name='provider',
            table='finance_provider',
        ),
        migrations.AlterModelTable(
            name='typelaunch',
            table='finance_typelaunch',
        ),
        migrations.AlterModelTable(
            name='weeknumber',
            table='finance_weeknumber',
        ),
    ]
