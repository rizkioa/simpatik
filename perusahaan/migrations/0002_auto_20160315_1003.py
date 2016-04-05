# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perusahaan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aktanotaris',
            name='jenis_akta',
            field=models.CharField(default=1, max_length=20, verbose_name=b'Jenis Akta', choices=[(b'Akta pendirian', b'AKTA PENDIRIAN'), (b'Akta pengesahan', b'AKTA PENGESAHAN')]),
        ),
    ]
