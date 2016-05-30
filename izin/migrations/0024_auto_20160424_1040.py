# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0023_auto_20160424_1030'),
    ]

    operations = [
        # migrations.AlterField(
        #     model_name='izin',
        #     name='jenis_gangguan',
        #     field=models.ManyToManyField(to='izin.JenisGangguan', verbose_name=b'Jenis Gangguan', blank=True),
        # ),
        # migrations.AlterField(
        #     model_name='izin',
        #     name='jenis_kegiatan_pembangunan',
        #     field=models.ManyToManyField(to='izin.JenisKegiatanPembangunan', verbose_name=b'Jenis Kegiatan Pembangunan', blank=True),
        # ),
        # migrations.AlterField(
        #     model_name='izin',
        #     name='parameter_bgunan',
        #     field=models.ManyToManyField(to='izin.ParameterBangunan', verbose_name=b'Parameter', blank=True),
        # ),
        migrations.AlterField(
            model_name='izin',
            name='pembaharuan',
            field=models.IntegerField(null=True, verbose_name=b'Pembaharuan', blank=True),
        ),
        migrations.AlterField(
            model_name='izin',
            name='pendaftaran',
            field=models.IntegerField(null=True, verbose_name=b'Pendaftaran', blank=True),
        ),
    ]
