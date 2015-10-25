# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0002_auto_20151015_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='sid',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
