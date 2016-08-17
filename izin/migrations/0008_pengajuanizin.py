# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('izin', '0007_auto_20160813_0738'),
    ]

    operations = [
        migrations.CreateModel(
            name='PengajuanIzin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.PositiveSmallIntegerField(default=6, verbose_name=b'Status Data', choices=[(1, b'Active'), (2, b'Inactive'), (3, b'Blocked'), (4, b'Submitted'), (5, b'Archive'), (6, b'Draft'), (7, b'Rejected')])),
                ('created_at', models.DateTimeField(editable=False)),
                ('verified_at', models.DateTimeField(editable=False)),
                ('rejected_at', models.DateTimeField(null=True, editable=False, blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(related_name='create_pengajuan_by_user', verbose_name=b'Dibuat Oleh', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('izin_induk', models.ForeignKey(blank=True, to='izin.PengajuanIzin', null=True)),
                ('jenis_permohonan', models.ForeignKey(verbose_name=b'Jenis Permohonan Izin', to='izin.JenisPermohonanIzin')),
                ('kelompok_jenis_izin', models.ForeignKey(verbose_name=b'Kelompok Jenis Izin', to='izin.KelompokJenisIzin')),
                ('pemohon', models.ForeignKey(related_name='pemohon_izin', blank=True, to='izin.Pemohon', null=True)),
                ('rejected_by', models.ForeignKey(related_name='rejected_pengajuan_by_user', verbose_name=b'Dibatalkan Oleh', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('verified_by', models.ForeignKey(related_name='verify_pengajuan_by_user', verbose_name=b'Diverifikasi Oleh', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-status', '-updated_at'],
                'verbose_name': 'Pengajuan Izin',
                'verbose_name_plural': 'Pengajuan Izin',
            },
        ),
    ]
