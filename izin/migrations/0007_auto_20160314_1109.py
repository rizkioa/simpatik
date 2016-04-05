# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0006_auto_20160312_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jeniskegiatanpembangunan',
            name='nilai',
            field=models.DecimalField(null=True, verbose_name=b'Nilai', max_digits=5, decimal_places=2, blank=True),
        ),
    ]
