# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0005_auto_20160601_1334'),
    ]

    operations = [
        migrations.AddField(
            model_name='jenispermohonanizin',
            name='jenis_izin',
            field=models.ForeignKey(default=1, verbose_name=b'Kelompok Jenis Izin', to='izin.KelompokJenisIzin'),
            preserve_default=False,
        ),
    ]
