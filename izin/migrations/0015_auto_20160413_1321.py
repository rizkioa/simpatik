# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0014_auto_20160316_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='izin',
            name='detil_papan_reklame',
            field=models.ForeignKey(verbose_name=b'Detil IMB Papan Reklame', blank=True, to='izin.DetilIMBPapanReklame', null=True),
        ),
        # migrations.AlterField(
        #     model_name='izin',
        #     name='jenis_gangguan',
        #     field=models.ManyToManyField(to='izin.JenisGangguan', null=True, verbose_name=b'Jenis Gangguan', blank=True),
        # ),
        # migrations.AlterField(
        #     model_name='izin',
        #     name='jenis_kegiatan_pembangunan',
        #     field=models.ManyToManyField(to='izin.JenisKegiatanPembangunan', null=True, verbose_name=b'Jenis Kegiatan Pembangunan', blank=True),
        # ),
        migrations.AlterField(
            model_name='izin',
            name='jenis_permohonan',
            field=models.ForeignKey(verbose_name=b'Jenis Permohonan Izin', blank=True, to='izin.JenisPermohonanIzin', null=True),
        ),
        migrations.AlterField(
            model_name='izin',
            name='kelompok_jenis_izin',
            field=models.ForeignKey(verbose_name=b'Kelompok Jenis Izin', blank=True, to='izin.KelompokJenisIzin', null=True),
        ),
        # migrations.AlterField(
        #     model_name='izin',
        #     name='parameter_bgunan',
        #     field=models.ManyToManyField(to='izin.ParameterBangunan', null=True, verbose_name=b'Parameter', blank=True),
        # ),
        migrations.AlterField(
            model_name='izin',
            name='pembaharuan',
            field=models.IntegerField(null=True, verbose_name=b'Pembaharuan', blank=True),
        ),
        migrations.AlterField(
            model_name='izin',
            name='pemohon',
            field=models.ForeignKey(related_name='pemohon_izin', blank=True, to='izin.Pemohon', null=True),
        ),
        migrations.AlterField(
            model_name='izin',
            name='pendaftaran',
            field=models.SmallIntegerField(null=True, verbose_name=b'Pendaftaran', blank=True),
        ),
    ]
