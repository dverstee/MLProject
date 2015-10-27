# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0004_auto_20151025_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='summoner',
            name='region',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='summoner_id',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='summoner',
            name='id',
            field=models.AutoField(primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='match',
            name='team1_is_red',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='preprocessedmatch',
            name='won',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='summoner',
            name='hotstreak',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='summoner',
            unique_together=set([('summoner_id', 'region')]),
        ),
    ]
