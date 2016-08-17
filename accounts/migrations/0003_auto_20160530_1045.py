# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_identitaspribadi_keterangan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identitaspribadi',
            name='telephone',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Telepon', blank=True),
        ),
    ]
