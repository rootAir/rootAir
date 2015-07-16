# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0012_weeknumber_docfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('opening', models.DateField(verbose_name='date open active')),
                ('time', models.DateTimeField(null=True, verbose_name='time execute active')),
                ('active', models.CharField(max_length=5)),
                ('operation', models.CharField(max_length=10)),
                ('type_operation', models.CharField(max_length=10)),
                ('quant_send', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quant_execut', models.DecimalField(decimal_places=2, max_digits=8)),
                ('price_send', models.DecimalField(decimal_places=2, max_digits=8)),
                ('price_execut', models.DecimalField(decimal_places=2, max_digits=8)),
                ('total', models.DecimalField(decimal_places=2, max_digits=8)),
                ('validate', models.DateField(verbose_name='validate operation')),
                ('status', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
