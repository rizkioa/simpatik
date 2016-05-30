# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perusahaan', '0003_auto_20160315_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perusahaan',
            name='jumlah_bank',
            field=models.IntegerField(null=True, verbose_name=b'Jumlah Bank', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='lg',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Longitute', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='lt',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Latitute', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='merk_dagang',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Merk Dagang', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='nama_kelompok_perusahaan',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Nama Kelompok Perusahaan', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='nasabah_utama_bank1',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Nasabah Utama Bank 1', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='nasabah_utama_bank2',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Nasabah Utama Bank 2', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='pemegang_hak_cipta',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Pemegang Hak Cipta', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='pemegang_hak_paten',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Pemegang Hak Paten', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='tanggal_mulai_kegiatan',
            field=models.DateField(null=True, verbose_name=b'Tanggal Mulai Kegiatan', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='tanggal_pendirian',
            field=models.DateField(null=True, verbose_name=b'Tanggal Pendirian', blank=True),
        ),
    ]
