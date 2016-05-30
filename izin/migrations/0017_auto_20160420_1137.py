# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0016_auto_20160413_1323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kekayaandansaham',
            name='izin',
            field=models.ForeignKey(verbose_name=b'Izin', blank=True, to='izin.Izin', null=True),
        ),
        migrations.AlterField(
            model_name='kekayaandansaham',
            name='kekayaan_bersih',
            field=models.DecimalField(null=True, verbose_name=b'Kekayaan Bersih', max_digits=10, decimal_places=2, blank=True),
        ),
    ]
