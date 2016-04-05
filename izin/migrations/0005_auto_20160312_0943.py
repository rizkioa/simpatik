# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0004_auto_20160312_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dasarhukum',
            name='keterangan',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True),
        ),
        migrations.AlterField(
            model_name='datareklame',
            name='lebar',
            field=models.DecimalField(null=True, verbose_name=b'Lebar', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='datareklame',
            name='panjang',
            field=models.DecimalField(null=True, verbose_name=b'Panjang', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='detilho',
            name='alamat',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Alamat', blank=True),
        ),
        migrations.AlterField(
            model_name='detilho',
            name='bahan_baku_dan_penolong',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Bahan Baku Dan Penolong', blank=True),
        ),
        migrations.AlterField(
            model_name='detilho',
            name='keperluan',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Keperluan', blank=True),
        ),
        migrations.AlterField(
            model_name='detilho',
            name='perkiraan_modal',
            field=models.DecimalField(null=True, verbose_name=b'Perkiraan Modal', max_digits=10, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='detilho',
            name='proses_produksi',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Proses Produksi', blank=True),
        ),
        migrations.AlterField(
            model_name='jenisgangguan',
            name='jenis_gangguan',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Jenis Gangguan', blank=True),
        ),
        migrations.AlterField(
            model_name='jenisizin',
            name='keterangan',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True),
        ),
        migrations.AlterField(
            model_name='jeniskegiatanpembangunan',
            name='jenis_kegiatan_pembangunan',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Jenis Kegiatan Pembangunan', blank=True),
        ),
        migrations.AlterField(
            model_name='jeniskegiatanpembangunan',
            name='nilai',
            field=models.IntegerField(null=True, verbose_name=b'Nilai', blank=True),
        ),
        migrations.AlterField(
            model_name='jenisperaturan',
            name='keterangan',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True),
        ),
        migrations.AlterField(
            model_name='jenispermohonanizin',
            name='jenis_permohonan_izin',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Jenis Permohonan Izin', blank=True),
        ),
        migrations.AlterField(
            model_name='jenistanah',
            name='jenis_tanah',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Jenis Tanah', blank=True),
        ),
        migrations.AlterField(
            model_name='kelompokjenisizin',
            name='keterangan',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True),
        ),
        migrations.AlterField(
            model_name='kepemilikkantanah',
            name='kepemilikan_tanah',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Kepemilikan Tanah', blank=True),
        ),
        migrations.AlterField(
            model_name='parameterbangunan',
            name='nilai',
            field=models.IntegerField(null=True, verbose_name=b'Nilai', blank=True),
        ),
        migrations.AlterField(
            model_name='parameterbangunan',
            name='parameter',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Parameter', blank=True),
        ),
        migrations.AlterField(
            model_name='prosedur',
            name='keterangan',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True),
        ),
        migrations.AlterField(
            model_name='statushaktanah',
            name='hak_tanah',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Hak Tanah', blank=True),
        ),
        migrations.AlterField(
            model_name='syarat',
            name='keterangan',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True),
        ),
        migrations.AlterField(
            model_name='verivikasiizin',
            name='nama_verifikasi',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Nama Verifikasi', blank=True),
        ),
    ]
