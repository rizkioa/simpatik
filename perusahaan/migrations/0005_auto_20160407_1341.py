# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perusahaan', '0004_auto_20160407_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perusahaan',
            name='fax',
            field=models.CharField(max_length=20, null=True, verbose_name=b'Fax', blank=True),
        ),
        migrations.AlterField(
            model_name='perusahaan',
            name='kode_pos',
            field=models.IntegerField(null=True, verbose_name=b'Kode Pos', blank=True),
        ),
    ]
