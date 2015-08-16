# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0008_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='supplier_city',
            field=models.CharField(default='erode', max_length=50),
            preserve_default=False,
        ),
    ]
