# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-19 19:39
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180319_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=jsonfield.fields.JSONField(),
        ),
    ]
