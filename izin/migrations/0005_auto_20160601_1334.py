# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0004_jenispermohonanizin'),
    ]

    operations = [
        migrations.AddField(
            model_name='prosedur',
            name='jenis_izin',
            field=models.ForeignKey(default=1, verbose_name=b'Kelompok Jenis Izin', to='izin.KelompokJenisIzin'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prosedur',
            name='nomor_urut',
            field=models.IntegerField(null=True, verbose_name=b'Nomor Urut', blank=True),
        ),
        migrations.AddField(
            model_name='syarat',
            name='jenis_izin',
            field=models.ForeignKey(default=1, verbose_name=b'Kelompok Jenis Izin', to='izin.KelompokJenisIzin'),
            preserve_default=False,
        ),
    ]
