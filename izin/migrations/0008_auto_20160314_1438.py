# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0007_auto_20160314_1109'),
    ]

    operations = [
        migrations.AddField(
            model_name='jeniskegiatanpembangunan',
            name='level',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jeniskegiatanpembangunan',
            name='lft',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jeniskegiatanpembangunan',
            name='rght',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jeniskegiatanpembangunan',
            name='tree_id',
            field=models.PositiveIntegerField(default=1, editable=False, db_index=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jenisizin',
            name='jenis_izin',
            field=models.CharField(default=1, max_length=20, verbose_name=b'Jenis Izin', choices=[(b'Izin Daerah', b'IZIN DAERAH'), (b'Izin Penanaman Modal', b'IZIN PENANAMAN MODAL')]),
        ),
    ]
