# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0018_auto_20160420_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jenisgangguan',
            name='jenis_gangguan',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Jenis Gangguan', blank=True),
        ),
    ]
