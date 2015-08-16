# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0003_moneyreceivedinformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneyreceivedinformation',
            name='remarks',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
