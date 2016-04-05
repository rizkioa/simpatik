# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Desa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_desa', models.CharField(max_length=40, null=True, verbose_name=b'Nama Desa')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan')),
                ('lt', models.CharField(max_length=100, null=True, verbose_name=b'Latitute')),
                ('lg', models.CharField(max_length=100, null=True, verbose_name=b'Longitute')),
            ],
            options={
                'verbose_name': 'Desa',
                'verbose_name_plural': 'Desa',
            },
        ),
        migrations.CreateModel(
            name='JenisNomorIdentitas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_nomor_identitas', models.CharField(max_length=30, verbose_name=b'Jenis Nomor Identitas')),
                ('keterangan', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Nomor Identitas',
                'verbose_name_plural': 'Jenis Nomor Identitas',
            },
        ),
        migrations.CreateModel(
            name='Kabupaten',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_kab', models.CharField(max_length=40, verbose_name=b'Kabupaten')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan')),
                ('lt', models.CharField(max_length=100, null=True, verbose_name=b'Latitute')),
                ('lg', models.CharField(max_length=100, null=True, verbose_name=b'Longitute')),
            ],
            options={
                'verbose_name': 'Kabupaten',
                'verbose_name_plural': 'Kabupaten',
            },
        ),
        migrations.CreateModel(
            name='Kecamatan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_kec', models.CharField(max_length=40, verbose_name=b'Kecamatan')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan')),
                ('lt', models.CharField(max_length=100, null=True, verbose_name=b'Latitute')),
                ('lg', models.CharField(max_length=100, null=True, verbose_name=b'Longitute')),
                ('nama_kab', models.ForeignKey(verbose_name=b'Kabupaten', to='master.Kabupaten')),
            ],
            options={
                'verbose_name': 'Kecamatan',
                'verbose_name_plural': 'Kecamatan',
            },
        ),
        migrations.CreateModel(
            name='Provinsi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_prov', models.CharField(max_length=40, verbose_name=b'Provinsi')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan')),
                ('lt', models.CharField(max_length=100, null=True, verbose_name=b'Latitute')),
                ('lg', models.CharField(max_length=100, null=True, verbose_name=b'Longitute')),
            ],
            options={
                'verbose_name': 'Provinsi',
                'verbose_name_plural': 'Provinsi',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parameter', models.CharField(max_length=100, verbose_name=b'Nama Parameter')),
                ('value', models.CharField(max_length=100, verbose_name=b'Nilai')),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Setting',
            },
        ),
        migrations.AddField(
            model_name='kabupaten',
            name='nama_prov',
            field=models.ForeignKey(verbose_name=b'Provinsi', to='master.Provinsi'),
        ),
        migrations.AddField(
            model_name='desa',
            name='nama_kec',
            field=models.ForeignKey(verbose_name=b'Kecamatan', to='master.Kecamatan'),
        ),
    ]
