# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0008_typeactivity_type_launch'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='synchronized',
            field=models.CharField(max_length=1, default='L', choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='typeactivity',
            name='synchronized',
            field=models.CharField(max_length=1, default='L', choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')]),
            preserve_default=False,
        ),
    ]
