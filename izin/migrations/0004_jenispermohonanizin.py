# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0003_kelompokjenisizin'),
    ]

    operations = [
        migrations.CreateModel(
            name='JenisPermohonanIzin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_permohonan_izin', models.CharField(max_length=255, verbose_name=b'Jenis Permohonan Izin')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Permohonan Izin',
                'verbose_name_plural': 'Jenis Permohonan Izin',
            },
        ),
    ]
