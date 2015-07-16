# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0016_weeknumber_value_transf'),
    ]

    operations = [
        migrations.RenameField(
            model_name='weeknumber',
            old_name='docfile',
            new_name='docfile_itau',
        ),
        migrations.AddField(
            model_name='weeknumber',
            name='docfile_mycap',
            field=models.FileField(default=0, upload_to='documents/%Y/%m/%d'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='weeknumber',
            name='value_prevision',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]
