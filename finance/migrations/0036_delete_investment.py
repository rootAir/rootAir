# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0035_auto_20150420_1548'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Investment',
        ),
    ]
