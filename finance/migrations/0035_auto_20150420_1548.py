# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0034_auto_20150413_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extract',
            name='synchronized',
            field=models.CharField(max_length=1, choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='investment',
            name='synchronized',
            field=models.CharField(max_length=1, choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='provider',
            name='synchronized',
            field=models.CharField(max_length=1, choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='typelaunch',
            name='synchronized',
            field=models.CharField(max_length=1, choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeknumber',
            name='docfile_itau',
            field=models.FileField(upload_to=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeknumber',
            name='docfile_mycap',
            field=models.FileField(upload_to=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeknumber',
            name='synchronized',
            field=models.CharField(max_length=1, choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')]),
            preserve_default=True,
        ),
    ]
