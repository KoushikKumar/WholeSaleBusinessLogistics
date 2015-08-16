# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0009_product_supplier_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoneyPaidInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('supplier_name', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('amount_paid', models.IntegerField()),
                ('remarks', models.CharField(max_length=100, blank=True)),
                ('date', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
