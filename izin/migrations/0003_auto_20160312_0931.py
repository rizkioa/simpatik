# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0002_auto_20160312_0844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jenisizin',
            name='jenis_izin',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Jenis Izin', blank=True),
        ),
    ]
