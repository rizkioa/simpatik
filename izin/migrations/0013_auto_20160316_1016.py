# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import izin.models


class Migration(migrations.Migration):

    dependencies = [
        ('perusahaan', '0003_auto_20160315_1108'),
        ('izin', '0012_auto_20160315_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Berkas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_berkas', models.CharField(max_length=100, verbose_name=b'Nama Berkas')),
                ('berkas', izin.models.FileField(max_length=255, upload_to=izin.models.PathAndRename(b'berkas/'))),
            ],
            options={
                'verbose_name': 'Berkas',
                'verbose_name_plural': 'Berkas',
            },
        ),
        migrations.CreateModel(
            name='JenisBerkas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_berkas', models.CharField(max_length=50, null=True, verbose_name=b'Jenis Berkas', blank=True)),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Berkas',
                'verbose_name_plural': 'Jenis Berkas',
            },
        ),
        migrations.AlterField(
            model_name='izin',
            name='pemohon',
            field=models.ForeignKey(related_name='pemohon_izin', to='izin.Pemohon'),
        ),
        migrations.AddField(
            model_name='berkas',
            name='jenis_berkas',
            field=models.ForeignKey(verbose_name=b'Jenis Berkas', blank=True, to='izin.JenisBerkas', null=True),
        ),
        migrations.AddField(
            model_name='berkas',
            name='pemohon',
            field=models.ForeignKey(related_name='pemohon_izin_berkas', to='izin.Pemohon'),
        ),
        migrations.AddField(
            model_name='berkas',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', to='perusahaan.Perusahaan'),
        ),
    ]
