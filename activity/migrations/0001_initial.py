# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('description', models.CharField(unique=True, max_length=100)),
                ('date_activity', models.DateField(verbose_name='date activity')),
                ('hour_init', models.DateTimeField(verbose_name='hour init')),
                ('hour_final', models.DateTimeField(verbose_name='hour final')),
                ('time_total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('calendar', models.CharField(unique=True, max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeActivity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('type_name', models.CharField(unique=True, max_length=10)),
                ('type_desc', models.CharField(unique=True, max_length=50)),
                ('group', models.CharField(unique=True, max_length=10)),
                ('have_cost', models.BooleanField(default=False, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='type_activity',
            field=models.ForeignKey(blank=True, to='activity.TypeActivity', null=True),
            preserve_default=True,
        ),
    ]
