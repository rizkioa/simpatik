# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prosedur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prosedur', models.CharField(max_length=255, verbose_name=b'Prosedur')),
                ('lama', models.PositiveSmallIntegerField(null=True, verbose_name=b'Lama (Berapa Hari?)', blank=True)),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Prosedur',
                'verbose_name_plural': 'Prosedur',
            },
        ),
        migrations.CreateModel(
            name='Syarat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('syarat', models.CharField(max_length=255, verbose_name=b'Syarat')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Syarat',
                'verbose_name_plural': 'Syarat',
            },
        ),
    ]
