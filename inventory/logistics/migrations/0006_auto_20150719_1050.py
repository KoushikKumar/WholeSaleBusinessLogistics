# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0005_moneyreceivedinformation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='loading_date',
            field=models.DateField(help_text=b'YYYY-MM-DD'),
        ),
    ]
