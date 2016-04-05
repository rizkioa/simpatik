# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models
import mptt.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('master', '__first__'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bidang',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_bidang', models.CharField(max_length=200, verbose_name=b'Organisasi di Bawah SKPD')),
                ('plt', models.BooleanField(default=False, verbose_name=b'Apakah PLT?')),
                ('keterangan', models.CharField(max_length=255, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Organisasi di Bawah SKPD',
                'verbose_name_plural': 'Organisasi di Bawah SKPD',
            },
        ),
        migrations.CreateModel(
            name='IdentitasPribadi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_lengkap', models.CharField(max_length=100, verbose_name=b'Nama Lengkap')),
                ('tempat_lahir', models.CharField(max_length=30, null=True, verbose_name=b'Tempat Lahir', blank=True)),
                ('tanggal_lahir', models.DateField(null=True, verbose_name=b'Tanggal Lahir', blank=True)),
                ('telephone', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, unique=True, null=True, blank=True)),
                ('alamat', models.CharField(max_length=255, null=True, blank=True)),
                ('lintang', models.CharField(max_length=255, null=True, verbose_name=b'Lintang', blank=True)),
                ('bujur', models.CharField(max_length=255, null=True, verbose_name=b'Bujur', blank=True)),
                ('kewarganegaraan', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Identitas Pribadi',
                'verbose_name_plural': 'Identitas Pribadi',
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
            name='NomorIdentitasPengguna',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nomor', models.CharField(unique=True, max_length=100)),
                ('jenis_identitas', models.ForeignKey(verbose_name=b'Jenis Nomor Identitas', to='master.JenisNomorIdentitas')),
            ],
            options={
                'verbose_name': 'Nomor Identitas Pengguna',
                'verbose_name_plural': 'Nomor Identitas Pengguna',
            },
        ),
        migrations.CreateModel(
            name='SKPD',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kode_satker', models.IntegerField(null=True, verbose_name=b'Kode Satker', blank=True)),
                ('nama_skpd', models.CharField(max_length=100, verbose_name=b'SKPD')),
                ('plt', models.BooleanField(default=False, verbose_name=b'Apakah PLT?')),
                ('keterangan', models.CharField(max_length=255, null=True, blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
            ],
            options={
                'verbose_name': 'SKPD',
                'verbose_name_plural': 'SKPD',
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('identitaspribadi_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='accounts.IdentitasPribadi')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=40)),
                ('foto', accounts.models.ImageField(max_length=255, null=True, upload_to=accounts.models.PathAndRename(b'profiles/'), blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name=b'Apakah Active?')),
                ('is_admin', models.BooleanField(default=False, verbose_name=b'Apakah Admin?')),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name=b'Status Data', choices=[(1, b'Active'), (2, b'Inactive'), (3, b'Blocked'), (4, b'Submitted'), (5, b'Archive')])),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Akun',
                'verbose_name_plural': 'Akun',
            },
            bases=('accounts.identitaspribadi', models.Model),
        ),
        migrations.AddField(
            model_name='skpd',
            name='kepala',
            field=models.ForeignKey(related_name='kepala', verbose_name=b'Kepala SKPD', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='nomoridentitaspengguna',
            name='user',
            field=models.ForeignKey(verbose_name=b'User', to='accounts.IdentitasPribadi'),
        ),
        migrations.AddField(
            model_name='identitaspribadi',
            name='desa',
            field=models.ForeignKey(verbose_name=b'Desa', to='master.Desa', null=True),
        ),
        migrations.AddField(
            model_name='bidang',
            name='kepala',
            field=models.ForeignKey(related_name='kepala_uptd', verbose_name=b'Kepala UPTD', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.CreateModel(
            name='Pegawai',
            fields=[
                ('account_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bidang', mptt.fields.TreeForeignKey(verbose_name=b'Bidang', to='accounts.Bidang')),
                ('jabatan', models.ForeignKey(verbose_name=b'Jabatan', to='accounts.Jabatan')),
                ('skpd', mptt.fields.TreeForeignKey(verbose_name=b'SKPD', to='accounts.SKPD')),
            ],
            options={
                'verbose_name': 'Pegawai',
                'verbose_name_plural': 'Pegawai',
            },
            bases=('accounts.account',),
        ),
        migrations.AddField(
            model_name='account',
            name='groups',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='account',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
