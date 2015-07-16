# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0019_auto_20150318_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='extract',
            name='synchronized',
            field=models.CharField(default='L', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='investment',
            name='synchronized',
            field=models.CharField(default='L', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='provider',
            name='synchronized',
            field=models.CharField(default='L', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='typelaunch',
            name='synchronized',
            field=models.CharField(default='L', max_length=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weeknumber',
            name='synchronized',
            field=models.CharField(default='L', max_length=1),
            preserve_default=False,
        ),
    ]
