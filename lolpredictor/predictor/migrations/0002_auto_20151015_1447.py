# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='preprocessedmatch',
            name='team_2_adc_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='preprocessedmatch',
            name='team_2_jungle_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='preprocessedmatch',
            name='team_2_mid_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='preprocessedmatch',
            name='team_2_supp_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='preprocessedmatch',
            name='team_2_top_score',
            field=models.FloatField(default=0),
        ),
    ]
