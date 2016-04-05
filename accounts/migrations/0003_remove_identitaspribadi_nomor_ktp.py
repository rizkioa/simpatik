# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_identitaspribadi_nomor_ktp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='identitaspribadi',
            name='nomor_ktp',
        ),
    ]
