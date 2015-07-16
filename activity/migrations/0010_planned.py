# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0009_auto_20150420_1548'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planned',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('date_activity', models.DateField(verbose_name='date activity')),
                ('hour_init', models.DateTimeField(blank=True, null=True, verbose_name='hour init')),
                ('hour_final', models.DateTimeField(blank=True, null=True, verbose_name='hour final')),
                ('time_total', models.DecimalField(decimal_places=2, blank=True, max_digits=8)),
                ('checked', models.BooleanField(default=False, db_index=True)),
                ('state', models.CharField(max_length=20)),
                ('check_list', models.CharField(max_length=50)),
                ('synchronized', models.CharField(choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')], max_length=1)),
                ('type_activity', models.ForeignKey(blank=True, to='activity.TypeActivity', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
