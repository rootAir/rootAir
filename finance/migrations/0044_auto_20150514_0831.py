# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0043_auto_20150514_0826'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='weeknumber',
            options={'managed': False},
        ),
    ]
