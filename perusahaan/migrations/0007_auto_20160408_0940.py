# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perusahaan', '0006_perusahaan_desa'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perusahaan',
            old_name='status_perusahaan',
            new_name='status_dari_perusahaan',
        ),
    ]
