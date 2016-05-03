# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '__first__'),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
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
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Akun',
                'verbose_name_plural': 'Akun',
            },
            bases=('accounts.identitaspribadi', models.Model),
        ),
        migrations.AddField(
            model_name='nomoridentitaspengguna',
            name='user',
            field=models.ForeignKey(verbose_name=b'User', to='accounts.IdentitasPribadi'),
        ),
        migrations.AddField(
            model_name='identitaspribadi',
            name='desa',
            field=models.ForeignKey(verbose_name=b'Desa', blank=True, to='master.Desa', null=True),
        ),
    ]
