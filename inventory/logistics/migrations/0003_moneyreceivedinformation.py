# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0002_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoneyReceivedInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_name', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('amount_paid', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
