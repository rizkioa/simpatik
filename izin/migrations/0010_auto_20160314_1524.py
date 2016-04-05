# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0009_jeniskegiatanpembangunan_jenis_kegiatan_induk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jeniskegiatanpembangunan',
            name='jenis_kegiatan_induk',
        ),
        migrations.RemoveField(
            model_name='jeniskegiatanpembangunan',
            name='level',
        ),
        migrations.RemoveField(
            model_name='jeniskegiatanpembangunan',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='jeniskegiatanpembangunan',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='jeniskegiatanpembangunan',
            name='tree_id',
        ),
    ]
