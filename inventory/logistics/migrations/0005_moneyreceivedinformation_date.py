# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0004_moneyreceivedinformation_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneyreceivedinformation',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 7, 19, 9, 37, 40, 800175, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
