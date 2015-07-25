# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0067_auto_20150614_2351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('nome', models.CharField(max_length=50, unique=True)),
                ('telefone', models.CharField(max_length=10, unique=True)),
                ('data', models.DateField(verbose_name='date contato')),
            ],
        ),
    ]
