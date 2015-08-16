# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product_name', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('weight', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('buying_price', models.IntegerField()),
                ('selling_price', models.IntegerField()),
                ('transport_price', models.IntegerField()),
                ('supplier', models.CharField(max_length=50)),
                ('loading_date', models.DateField()),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
