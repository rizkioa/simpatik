# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jenisizin',
            name='kelompok_izin',
        ),
        migrations.AddField(
            model_name='kelompokjenisizin',
            name='jenis_izin',
            field=models.ForeignKey(default=1, verbose_name=b'Jenis Izin', to='izin.JenisIzin'),
            preserve_default=False,
        ),
    ]
