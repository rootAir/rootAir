# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0066_auto_20150604_0425'),
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='weeknumber',
            name='operation_broker',
            field=models.DecimalField(decimal_places=2, null=True, max_digits=8, blank=True),
        ),
    ]
