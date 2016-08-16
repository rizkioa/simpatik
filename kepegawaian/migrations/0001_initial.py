# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20160530_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='BidangStruktural',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_bidang', models.CharField(max_length=200, verbose_name=b'Bagian / Bidang / Seksi (Struktural)')),
                ('keterangan', models.CharField(max_length=255, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('bidang_induk', mptt.fields.TreeForeignKey(verbose_name=b'Bidang Induk', blank=True, to='kepegawaian.BidangStruktural', null=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Bagian / Bidang / Seksi (Struktural)',
                'verbose_name_plural': 'Bagian / Bidang / Seksi (Struktural)',
            },
        ),
        migrations.CreateModel(
            name='Jabatan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_jabatan', models.CharField(max_length=50, verbose_name=b'Nama Jabatan')),
                ('keterangan', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jabatan',
                'verbose_name_plural': 'Jabatan',
            },
        ),
        migrations.CreateModel(
            name='JenisUnitKerja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_unit_kerja', models.CharField(max_length=30, verbose_name=b'Jenis Unit Kerja')),
                ('keterangan', models.CharField(max_length=255, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('jenis_unit_kerja_induk', mptt.fields.TreeForeignKey(verbose_name=b'Jenis Unit Kerja Induk', blank=True, to='kepegawaian.JenisUnitKerja', null=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Unit Kerja',
                'verbose_name_plural': 'Jenis Unit Kerja',
            },
        ),
        migrations.CreateModel(
            name='Pegawai',
            fields=[
                ('account_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bidang_struktural', mptt.fields.TreeForeignKey(verbose_name=b'Bagian / Bidang / Seksi (Struktural)', to='kepegawaian.BidangStruktural')),
                ('jabatan', models.ForeignKey(verbose_name=b'Jabatan', to='kepegawaian.Jabatan')),
            ],
            options={
                'verbose_name': 'Pegawai',
                'verbose_name_plural': 'Pegawai',
            },
            bases=('accounts.account',),
        ),
        migrations.CreateModel(
            name='UnitKerja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_unit_kerja', models.CharField(max_length=100, verbose_name=b'Unit Kerja')),
                ('keterangan', models.CharField(max_length=255, null=True, blank=True)),
                ('kode_rekening', models.CharField(default=b'xx', max_length=15, null=True, verbose_name=b'Kode Rekening', blank=True)),
                ('plt', models.BooleanField(default=False, verbose_name=b'Apakah PLT?')),
                ('telephone', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=50, null=True, blank=True)),
                ('alamat', models.CharField(max_length=255, null=True, blank=True)),
                ('kode_pos', models.CharField(max_length=50, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('jenis_unit_kerja', models.ForeignKey(related_name='unit_kerja_jenis', verbose_name=b'Jenis Unit Kerja', blank=True, to='kepegawaian.JenisUnitKerja', null=True)),
                ('kepala', models.ForeignKey(related_name='kepala', verbose_name=b'Kepala Unit Kerja', blank=True, to='kepegawaian.Pegawai', null=True)),
                ('unit_kerja_induk', mptt.fields.TreeForeignKey(verbose_name=b'Unit Kerja Induk', blank=True, to='kepegawaian.UnitKerja', null=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Unit Kerja',
                'verbose_name_plural': 'Unit Kerja',
            },
        ),
        migrations.AddField(
            model_name='pegawai',
            name='unit_kerja',
            field=mptt.fields.TreeForeignKey(verbose_name=b'Unit Kerja', to='kepegawaian.UnitKerja'),
        ),
        migrations.AddField(
            model_name='bidangstruktural',
            name='unit_kerja',
            field=mptt.fields.TreeForeignKey(verbose_name=b'Unit Kerja', to='kepegawaian.UnitKerja'),
        ),
    ]
