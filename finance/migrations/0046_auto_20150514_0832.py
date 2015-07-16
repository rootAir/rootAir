# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0045_auto_20150514_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeknumber',
            name='id',
            field=models.IntegerField(serialize=False, primary_key=True),
        ),
    ]
