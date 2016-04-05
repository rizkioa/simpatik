# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='identitaspribadi',
            name='nomor_ktp',
            field=models.CharField(max_length=15, null=True, verbose_name=b'Nomor KTP', blank=True),
        ),
    ]
