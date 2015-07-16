# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0030_auto_20150413_2207'),
    ]

    operations = [
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
    ]
