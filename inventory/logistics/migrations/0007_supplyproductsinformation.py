# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0006_auto_20150719_1050'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplyProductsInformation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_name', models.CharField(max_length=30)),
                ('city', models.CharField(max_length=30)),
                ('product_name', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('weight', models.IntegerField()),
                ('selling_price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('date', models.DateField()),
                ('remarks', models.CharField(max_length=100, blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
