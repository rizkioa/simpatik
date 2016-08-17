# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0006_jenispermohonanizin_jenis_izin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jenispermohonanizin',
            name='jenis_izin',
        ),
        migrations.AddField(
            model_name='jenispermohonanizin',
            name='jenis_izin',
            field=models.ManyToManyField(to='izin.KelompokJenisIzin', verbose_name=b'Kelompok Jenis Izin'),
        ),
    ]
