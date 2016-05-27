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
                ('nama_desa', models.CharField(max_length=40, null=True, verbose_name=b'Nama Desa / Kelurahan')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
                ('lt', models.CharField(max_length=100, null=True, verbose_name=b'Latitute', blank=True)),
                ('lg', models.CharField(max_length=100, null=True, verbose_name=b'Longitute', blank=True)),
            ],
            options={
                'ordering': ['nama_desa'],
                'verbose_name': 'Desa / Kelurahan',
                'verbose_name_plural': 'Desa / Kelurahan',
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
                ('nama_kabupaten', models.CharField(max_length=40, verbose_name=b'Kabupaten / Kota')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
                ('lt', models.CharField(max_length=100, null=True, verbose_name=b'Latitute', blank=True)),
                ('lg', models.CharField(max_length=100, null=True, verbose_name=b'Longitute', blank=True)),
            ],
            options={
                'ordering': ['nama_kabupaten'],
                'verbose_name': 'Kabupaten / Kota',
                'verbose_name_plural': 'Kabupaten / Kota',
            },
        ),
        migrations.CreateModel(
            name='Kecamatan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_kecamatan', models.CharField(max_length=40, verbose_name=b'Kecamatan')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
                ('lt', models.CharField(max_length=100, null=True, verbose_name=b'Latitute', blank=True)),
                ('lg', models.CharField(max_length=100, null=True, verbose_name=b'Longitute', blank=True)),
                ('kabupaten', models.ForeignKey(verbose_name=b'Kabupaten / Kota', to='master.Kabupaten')),
            ],
            options={
                'ordering': ['nama_kecamatan'],
                'verbose_name': 'Kecamatan',
                'verbose_name_plural': 'Kecamatan',
            },
        ),
        migrations.CreateModel(
            name='Negara',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_negara', models.CharField(max_length=40, verbose_name=b'Negara')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
                ('code', models.CharField(max_length=10, null=True, verbose_name=b'Kode Negara', blank=True)),
                ('lt', models.CharField(max_length=100, null=True, verbose_name=b'Latitute', blank=True)),
                ('lg', models.CharField(max_length=100, null=True, verbose_name=b'Longitute', blank=True)),
            ],
            options={
                'ordering': ['nama_negara'],
                'verbose_name': 'Negara',
                'verbose_name_plural': 'Negara',
            },
        ),
        migrations.CreateModel(
            name='Provinsi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_provinsi', models.CharField(max_length=40, verbose_name=b'Provinsi')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
                ('lt', models.CharField(max_length=100, null=True, verbose_name=b'Latitute', blank=True)),
                ('lg', models.CharField(max_length=100, null=True, verbose_name=b'Longitute', blank=True)),
                ('negara', models.ForeignKey(verbose_name=b'Negara', to='master.Negara')),
            ],
            options={
                'ordering': ['nama_provinsi'],
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
            name='provinsi',
            field=models.ForeignKey(verbose_name=b'Provinsi', to='master.Provinsi'),
        ),
        migrations.AddField(
            model_name='desa',
            name='kecamatan',
            field=models.ForeignKey(verbose_name=b'Kecamatan', to='master.Kecamatan'),
        ),
    ]
