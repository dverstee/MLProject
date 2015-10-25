# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0003_auto_20151025_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='summoner',
            name='account_id',
        ),
        migrations.RemoveField(
            model_name='summoner',
            name='sid',
        ),
        migrations.AddField(
            model_name='summoner',
            name='summoner_id',
            field=models.IntegerField(default=0, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='summoner',
            name='region',
            field=models.CharField(max_length=20, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
