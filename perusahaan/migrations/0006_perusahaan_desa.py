# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0001_initial'),
        ('perusahaan', '0005_auto_20160407_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='perusahaan',
            name='desa',
            field=models.ForeignKey(verbose_name=b'Desa', blank=True, to='master.Desa', null=True),
        ),
    ]
