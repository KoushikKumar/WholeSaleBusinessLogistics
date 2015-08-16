# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0010_moneypaidinformation'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiscellaneousExpenditureInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expenditure_amount', models.IntegerField()),
                ('remarks', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
