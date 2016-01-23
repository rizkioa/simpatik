# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JenisNomorIdentitas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_nomor_identitas', models.CharField(max_length=30, verbose_name=b'Jenis Nomor Identitas')),
                ('keterangan', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Nomor Identitas',
                'verbose_name_plural': 'Jenis Nomor Identitas',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parameter', models.CharField(max_length=100, verbose_name=b'Nama Parameter')),
                ('value', models.CharField(max_length=100, verbose_name=b'Nilai')),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Setting',
            },
        ),
    ]
