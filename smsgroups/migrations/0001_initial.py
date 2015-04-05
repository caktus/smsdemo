# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('rapidsms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_creator', models.BooleanField(default=False)),
                ('joined_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('contact', models.ForeignKey(to='rapidsms.Contact')),
                ('group', models.ForeignKey(to='smsgroups.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
