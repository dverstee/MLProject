# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0008_apikey'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apikey',
            name='id',
        ),
        migrations.AlterField(
            model_name='apikey',
            name='key',
            field=models.CharField(max_length=36, serialize=False, primary_key=True),
        ),
    ]
