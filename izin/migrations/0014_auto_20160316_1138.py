# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('izin', '0013_auto_20160316_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='berkas',
            name='pemohon',
            field=models.ForeignKey(related_name='pemohon_izin_berkas', to='izin.Pemohon', null=True),
        ),
        migrations.AlterField(
            model_name='berkas',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', to='perusahaan.Perusahaan', null=True),
        ),
    ]
