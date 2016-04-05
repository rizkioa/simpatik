# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perusahaan', '0002_auto_20160315_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jeniskedudukan',
            name='kedudukan',
            field=models.CharField(default=1, choices=[(b'dirut/ dir cabang/penanggung jawab', b'Dirut/ Dir cabang/Penanggung jawab'), (b'direktur', b'Direktur'), (b'komisaris', b'Komisaris')], max_length=50, blank=True, null=True, verbose_name=b'Kedudukan'),
        ),
    ]
