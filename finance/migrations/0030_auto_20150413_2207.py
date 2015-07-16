# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0029_auto_20150410_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='total_debit_week',
            field=models.DecimalField(max_digits=8, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeknumber',
            name='docfile_itau',
            field=models.FileField(upload_to='tmp/%Y/%m/%d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='weeknumber',
            name='docfile_mycap',
            field=models.FileField(upload_to='tmp/%Y/%m/%d'),
            preserve_default=True,
        ),
    ]
