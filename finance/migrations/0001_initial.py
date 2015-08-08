# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Balance',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contato',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('nome', models.CharField(unique=True, max_length=50)),
                ('telefone', models.CharField(unique=True, max_length=10)),
                ('data', models.DateField(verbose_name='date contato')),
            ],
            options={
                'ordering': ['nome'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Extract',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('date_launch', models.DateField(verbose_name='date launch')),
                ('launch', models.CharField(max_length=100)),
                ('date_purchase', models.DateField(verbose_name='date purchase')),
                ('value_debit', models.DecimalField(decimal_places=2, max_digits=8)),
                ('value_credit', models.DecimalField(decimal_places=2, max_digits=8)),
                ('value_balance', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cancelled', models.BooleanField(db_index=True, default=True)),
                ('synchronized', models.CharField(choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')], max_length=1)),
            ],
            options={
                'db_table': 'finance_extract',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Prevision',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('description', models.CharField(unique=True, max_length=100)),
                ('date_expiration', models.DateField(verbose_name='date expiration')),
                ('debit_prevision', models.DecimalField(decimal_places=2, max_digits=8)),
                ('credit_prevision', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_payment', models.DateField(blank=True, null=True, verbose_name='date payment')),
                ('synchronized', models.CharField(null=True, choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')], blank=True, max_length=1)),
                ('observation', models.TextField()),
                ('paid', models.BooleanField(db_index=True, default=False)),
            ],
            options={
                'db_table': 'finance_prevision',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('description', models.CharField(unique=True, max_length=100)),
                ('date_last_purchase', models.DateField(verbose_name='date last purchase')),
                ('total_debit_week', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total_credit_week', models.DecimalField(decimal_places=2, max_digits=8)),
                ('synchronized', models.CharField(choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')], max_length=1)),
                ('observation', models.TextField()),
            ],
            options={
                'db_table': 'finance_provider',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WeekNumber',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('num_week', models.IntegerField()),
                ('date_closed', models.DateTimeField(blank=True, null=True, verbose_name='date time closed')),
                ('value_week', models.DecimalField(decimal_places=2, max_digits=8)),
                ('value_debit_week', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_init', models.DateField(verbose_name='date initial week')),
                ('date_final', models.DateField(verbose_name='date final week')),
                ('value_credit_week', models.DecimalField(decimal_places=2, max_digits=8)),
                ('close_week', models.BooleanField(db_index=True, default=False)),
                ('value_invest', models.DecimalField(decimal_places=2, max_digits=8)),
                ('value_transf', models.DecimalField(decimal_places=2, max_digits=8)),
                ('value_trade', models.DecimalField(decimal_places=2, max_digits=8)),
                ('docfile_mycap', models.FileField(upload_to='')),
                ('docfile_itau', models.FileField(upload_to='')),
                ('quant_trade', models.IntegerField()),
                ('tax_trade', models.DecimalField(decimal_places=2, max_digits=8)),
                ('percent_result', models.CharField(blank=True, max_length=8)),
                ('synchronized', models.CharField(choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')], max_length=1)),
                ('cost_fixed_week', models.DecimalField(decimal_places=2, max_digits=8)),
                ('available_broker', models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=8)),
                ('operation_broker', models.DecimalField(decimal_places=2, blank=True, null=True, max_digits=8)),
            ],
            options={
                'db_table': 'finance_weeknumber',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='prevision',
            name='provider',
            field=models.ForeignKey(blank=True, to='finance.Provider', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='extract',
            name='provider',
            field=models.ForeignKey(blank=True, to='finance.Provider', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='TypeLaunch',
            fields=[
            ],
            options={
                'db_table': 'finance_typelaunch',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='provider',
            name='type_launch',
            field=models.ForeignKey(blank=True, to='finance.TypeLaunch', null=True),
            preserve_default=True,
        ),
    ]
