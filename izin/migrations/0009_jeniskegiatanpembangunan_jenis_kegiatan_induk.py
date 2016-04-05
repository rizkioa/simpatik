# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0008_auto_20160314_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='jeniskegiatanpembangunan',
            name='jenis_kegiatan_induk',
            field=mptt.fields.TreeForeignKey(verbose_name=b'Jenis Kegiatan Pembangunan Induk', blank=True, to='izin.JenisKegiatanPembangunan', null=True),
        ),
    ]
