# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_identitaspribadi_nomor_ktp'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidang',
            name='bidang_induk',
            field=mptt.fields.TreeForeignKey(verbose_name=b'Bidang Induk', blank=True, to='accounts.Bidang', null=True),
        ),
        migrations.AddField(
            model_name='skpd',
            name='skpd_induk',
            field=mptt.fields.TreeForeignKey(verbose_name=b'SKPD Induk', blank=True, to='accounts.SKPD', null=True),
        ),
    ]
