# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perusahaan', '0009_auto_20160414_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produkutama',
            name='barang_jasa_utama',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Barang Jasa Utama', blank=True),
        ),
    ]
