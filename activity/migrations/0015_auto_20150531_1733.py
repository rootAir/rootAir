# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0014_auto_20150516_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeactivity',
            name='group',
            field=models.CharField(choices=[('Task', 'Task'), ('Sport', 'Sport'), ('Fun', 'Fun'), ('Study', 'Study'), ('Person', 'Person')], max_length=10),
        ),
    ]
