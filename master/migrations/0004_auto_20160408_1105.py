# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_auto_20160408_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desa',
            name='lg',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Longitute', blank=True),
        ),
        migrations.AlterField(
            model_name='desa',
            name='lt',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Latitute', blank=True),
        ),
        migrations.AlterField(
            model_name='kabupaten',
            name='lg',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Longitute', blank=True),
        ),
        migrations.AlterField(
            model_name='kabupaten',
            name='lt',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Latitute', blank=True),
        ),
        migrations.AlterField(
            model_name='kecamatan',
            name='lg',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Longitute', blank=True),
        ),
        migrations.AlterField(
            model_name='kecamatan',
            name='lt',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Latitute', blank=True),
        ),
        migrations.AlterField(
            model_name='provinsi',
            name='lg',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Longitute', blank=True),
        ),
        migrations.AlterField(
            model_name='provinsi',
            name='lt',
            field=models.CharField(max_length=100, null=True, verbose_name=b'Latitute', blank=True),
        ),
    ]
