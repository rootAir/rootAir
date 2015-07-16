# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0031_auto_20150413_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weeknumber',
            name='docfile_itau',
            field=models.FileField(upload_to='tmp'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeknumber',
            name='docfile_mycap',
            field=models.FileField(upload_to='tmp'),
            preserve_default=True,
        ),
    ]
