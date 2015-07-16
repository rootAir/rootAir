# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0059_auto_20150528_1250'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prevision',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('description', models.CharField(max_length=100, unique=True)),
                ('date_expiration', models.DateField(verbose_name='date expiration')),
                ('debit_prevision', models.DecimalField(decimal_places=2, max_digits=8)),
                ('credit_prevision', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_payment', models.DateField(verbose_name='date payment')),
                ('synchronized', models.CharField(choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')], blank=True, max_length=1, null=True)),
                ('observation', models.TextField()),
                ('provider', models.ForeignKey(to='finance.Provider', blank=True, null=True)),
            ],
            options={
                'db_table': 'finance_prevision',
            },
        ),
        migrations.AlterField(
            model_name='weeknumber',
            name='date_closed',
            field=models.DateTimeField(verbose_name='date time closed', blank=True, null=True),
        ),
    ]
