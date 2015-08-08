# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planned',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('description', models.CharField(max_length=500)),
                ('date_activity', models.DateField(verbose_name='date activity')),
                ('hour_init', models.DateTimeField(null=True, verbose_name='hour init', blank=True)),
                ('hour_final', models.DateTimeField(null=True, verbose_name='hour final', blank=True)),
                ('num_week', models.IntegerField(null=True, blank=True)),
                ('time_total', models.DecimalField(decimal_places=2, blank=True, max_digits=8)),
                ('checked', models.BooleanField(db_index=True, default=False)),
                ('state', models.CharField(max_length=20)),
                ('check_list', models.CharField(max_length=50)),
                ('synchronized', models.CharField(null=True, max_length=1, blank=True, choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')])),
            ],
            options={
                'db_table': 'activity_planned',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypeActivity',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('type_name', models.CharField(max_length=10, unique=True)),
                ('type_desc', models.CharField(max_length=50)),
                ('group', models.CharField(max_length=10, choices=[('Task', 'Task'), ('Sport', 'Sport'), ('Fun', 'Fun'), ('Study', 'Study'), ('Person', 'Person')])),
                ('positive', models.BooleanField(db_index=True, default=False)),
                ('synchronized', models.CharField(max_length=1, choices=[('L', 'Local'), ('H', 'Heroku'), ('S', 'Sync')])),
                ('type_launch', models.ForeignKey(null=True, to='finance.TypeLaunch', blank=True)),
            ],
            options={
                'db_table': 'activity_typeactivity',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='planned',
            name='type_activity',
            field=models.ForeignKey(null=True, to='activity.TypeActivity', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
            ],
            options={
                'db_table': 'activity_activity',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
