# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='desa',
            old_name='nama_kec',
            new_name='kecamatan',
        ),
        migrations.RenameField(
            model_name='kabupaten',
            old_name='nama_kab',
            new_name='nama_kabupaten',
        ),
        migrations.RenameField(
            model_name='kabupaten',
            old_name='nama_prov',
            new_name='provinsi',
        ),
        migrations.RenameField(
            model_name='kecamatan',
            old_name='nama_kab',
            new_name='Kabupaten',
        ),
        migrations.RenameField(
            model_name='kecamatan',
            old_name='nama_kec',
            new_name='nama_kecamatan',
        ),
        migrations.RenameField(
            model_name='provinsi',
            old_name='nama_prov',
            new_name='nama_provinsi',
        ),
    ]
