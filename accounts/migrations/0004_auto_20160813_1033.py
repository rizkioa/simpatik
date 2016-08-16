# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20160530_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='identitaspribadi',
            name='pekerjaan',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.PositiveSmallIntegerField(default=1, verbose_name=b'Status Data', choices=[(1, b'Active'), (2, b'Inactive'), (3, b'Blocked'), (4, b'Submitted'), (5, b'Archive'), (6, b'Draft'), (7, b'Rejected')]),
        ),
    ]
