# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20160314_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identitaspribadi',
            name='desa',
            field=models.ForeignKey(verbose_name=b'Desa', blank=True, to='master.Desa', null=True),
        ),
    ]
