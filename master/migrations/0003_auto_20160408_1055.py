# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0002_auto_20160408_1042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kecamatan',
            old_name='Kabupaten',
            new_name='kabupaten',
        ),
    ]
