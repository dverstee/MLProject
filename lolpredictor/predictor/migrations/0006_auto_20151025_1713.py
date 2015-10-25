# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0005_auto_20151025_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
