# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perusahaan', '0008_auto_20160408_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aktanotaris',
            name='jenis_akta',
            field=models.CharField(default=1, choices=[(b'Akta pendirian', b'AKTA PENDIRIAN'), (b'Akta pengesahan', b'AKTA PENGESAHAN')], max_length=20, blank=True, null=True, verbose_name=b'Jenis Akta'),
        ),
        migrations.AlterField(
            model_name='aktanotaris',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', blank=True, to='perusahaan.Perusahaan', null=True),
        ),
        migrations.AlterField(
            model_name='aktanotaris',
            name='tanggal_pengesahan',
            field=models.DateField(null=True, verbose_name=b'Tanggal Pengesahan', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='jumlah_karyawan_wna',
            field=models.IntegerField(null=True, verbose_name=b'Jumlah Karyawan WNA', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='jumlah_karyawan_wni',
            field=models.IntegerField(null=True, verbose_name=b'Jumlah Karyawan WNI', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='jumlah_saham',
            field=models.IntegerField(null=True, verbose_name=b'Jumlah Saham', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='kapasitas_mesin_terpasang',
            field=models.IntegerField(null=True, verbose_name=b'Kapasitas Mesin Terpasang', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='kapasitas_produksi_pertahun',
            field=models.IntegerField(null=True, verbose_name=b'Kapasitas Produksi Per Tahun', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='modal_dasar',
            field=models.IntegerField(null=True, verbose_name=b'Modal Dasar', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='modal_disetor',
            field=models.IntegerField(null=True, verbose_name=b'Modal Disetor', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='modal_ditempatkan',
            field=models.IntegerField(null=True, verbose_name=b'Modal Ditempatkan', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='nilai_saham_per_lembar',
            field=models.IntegerField(null=True, verbose_name=b'Nilai Saham Per Lembar', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='presentase_kandungan_komponen_produk_import',
            field=models.DecimalField(null=True, verbose_name=b'Presentase Kandungan Komponen Produk Import', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='presentase_kandungan_komponen_produk_lokal',
            field=models.DecimalField(null=True, verbose_name=b'Presentase Kandungan Komponen Produk Lokal', max_digits=5, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='stuan_kapasitas_msin_terpasang',
            field=models.CharField(max_length=10, null=True, verbose_name=b'Satuan Kapasitas Mesin Terpasang', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='stuan_kapasitas_produksi',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Satuan Kapasitas Produksi', blank=True),
        ),
        migrations.AlterField(
            model_name='datarincianperusahaan',
            name='total_aset',
            field=models.IntegerField(null=True, verbose_name=b'Total Aset', blank=True),
        ),
        migrations.AlterField(
            model_name='lokasiunitproduksi',
            name='alamat',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Alamat', blank=True),
        ),
        migrations.AlterField(
            model_name='lokasiunitproduksi',
            name='desa',
            field=models.ForeignKey(verbose_name=b'Desa', blank=True, to='master.Desa', null=True),
        ),
        migrations.AlterField(
            model_name='lokasiunitproduksi',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', blank=True, to='perusahaan.Perusahaan', null=True),
        ),
        migrations.AlterField(
            model_name='mesinhuller',
            name='jenis',
            field=models.ForeignKey(verbose_name=b'Jenis Mesin', blank=True, to='perusahaan.JenisMesin', null=True),
        ),
        migrations.AlterField(
            model_name='mesinperusahaan',
            name='PK',
            field=models.CharField(max_length=255, null=True, verbose_name=b'PK', blank=True),
        ),
        migrations.AlterField(
            model_name='mesinperusahaan',
            name='jumlah_unit',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Jumlah Unit', blank=True),
        ),
        migrations.AlterField(
            model_name='mesinperusahaan',
            name='kapasitas',
            field=models.IntegerField(null=True, verbose_name=b'Kapasitas', blank=True),
        ),
        migrations.AlterField(
            model_name='mesinperusahaan',
            name='merk',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Merk', blank=True),
        ),
        migrations.AlterField(
            model_name='mesinperusahaan',
            name='mesin',
            field=models.ForeignKey(verbose_name=b'Mesin Huller', blank=True, to='perusahaan.MesinHuller', null=True),
        ),
        migrations.AlterField(
            model_name='mesinperusahaan',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', blank=True, to='perusahaan.Perusahaan', null=True),
        ),
        migrations.AlterField(
            model_name='mesinperusahaan',
            name='tipe',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Type', blank=True),
        ),
        migrations.AlterField(
            model_name='modalkoprasi',
            name='jenis_modal',
            field=models.ForeignKey(verbose_name=b'Jenis Modal Koprasi', blank=True, to='perusahaan.JenisModalKoprasi', null=True),
        ),
        migrations.AlterField(
            model_name='nilaimodal',
            name='modal',
            field=models.ForeignKey(verbose_name=b'Modal Koprasi', blank=True, to='perusahaan.ModalKoprasi', null=True),
        ),
        migrations.AlterField(
            model_name='nilaimodal',
            name='nilai',
            field=models.IntegerField(null=True, verbose_name=b'Modal Koprasi', blank=True),
        ),
        migrations.AlterField(
            model_name='nilaimodal',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', blank=True, to='perusahaan.Perusahaan', null=True),
        ),
        migrations.AlterField(
            model_name='pemegangsahamlain',
            name='jumlah_modal_disetor',
            field=models.IntegerField(null=True, verbose_name=b'Jumlah Modal Disetor', blank=True),
        ),
        migrations.AlterField(
            model_name='pemegangsahamlain',
            name='jumlah_saham_dimiliki',
            field=models.IntegerField(null=True, verbose_name=b'Jumlah Saham Dimiliki', blank=True),
        ),
        migrations.AlterField(
            model_name='pemegangsahamlain',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', blank=True, to='perusahaan.Perusahaan', null=True),
        ),
        migrations.AlterField(
            model_name='produkutama',
            name='kelembagaan',
            field=models.ForeignKey(verbose_name=b'Kelembagaan', blank=True, to='perusahaan.Kelembagaan', null=True),
        ),
        migrations.AlterField(
            model_name='produkutama',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', blank=True, to='perusahaan.Perusahaan', null=True),
        ),
    ]
