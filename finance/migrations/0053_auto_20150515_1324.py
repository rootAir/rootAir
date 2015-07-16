# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0052_provider_observation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='observation',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
