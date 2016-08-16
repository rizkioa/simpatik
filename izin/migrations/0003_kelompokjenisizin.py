# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0002_prosedur_syarat'),
    ]

    operations = [
        migrations.CreateModel(
            name='KelompokJenisIzin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kelompok_jenis_izin', models.CharField(max_length=100, verbose_name=b'Kelompok Jenis Izin')),
                ('biaya', models.DecimalField(default=Decimal('0.00'), verbose_name=b'Biaya', max_digits=10, decimal_places=2)),
                ('standart_waktu', models.PositiveSmallIntegerField(null=True, verbose_name=b'Standar Waktu (Berapa Hari?)', blank=True)),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
                ('jenis_izin', models.ForeignKey(verbose_name=b'Jenis Izin', to='izin.JenisIzin')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Kelompok Jenis Izin',
                'verbose_name_plural': 'Kelompok Jenis Izin',
            },
        ),
    ]
