# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import izin.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20160530_1045'),
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DasarHukum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instansi', models.CharField(max_length=100, verbose_name=b'Instansi')),
                ('nomor', models.CharField(max_length=100, verbose_name=b'Nomor')),
                ('tahun', models.PositiveSmallIntegerField(choices=[(2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971), (1970, 1970), (1969, 1969), (1968, 1968), (1967, 1967), (1966, 1966), (1965, 1965), (1964, 1964), (1963, 1963), (1962, 1962), (1961, 1961), (1960, 1960), (1959, 1959), (1958, 1958), (1957, 1957), (1956, 1956), (1955, 1955), (1954, 1954), (1953, 1953), (1952, 1952), (1951, 1951), (1950, 1950), (1949, 1949), (1948, 1948), (1947, 1947), (1946, 1946), (1945, 1945)])),
                ('tentang', models.CharField(max_length=255, verbose_name=b'Tentang')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
                ('berkas', izin.models.FileField(max_length=255, null=True, upload_to=izin.models.PathAndRename(b'peraturan/'), blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Dasar Hukum',
                'verbose_name_plural': 'Dasar Hukum',
            },
        ),
        migrations.CreateModel(
            name='JenisIzin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_izin', models.CharField(max_length=100, verbose_name=b'Nama Izin')),
                ('jenis_izin', models.CharField(default=1, max_length=20, verbose_name=b'Jenis Izin', choices=[(b'Izin Daerah', b'IZIN DAERAH'), (b'Izin Penanaman Modal', b'IZIN PENANAMAN MODAL')])),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
                ('dasar_hukum', models.ManyToManyField(to='izin.DasarHukum', verbose_name=b'Dasar Hukum')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Izin',
                'verbose_name_plural': 'Jenis Izin',
            },
        ),
        migrations.CreateModel(
            name='JenisPeraturan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_peraturan', models.CharField(max_length=100, verbose_name=b'Jenis Peraturan')),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Peraturan',
                'verbose_name_plural': 'Jenis Peraturan',
            },
        ),
        migrations.CreateModel(
            name='Pemohon',
            fields=[
                ('account_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('jabatan_pemohon', models.CharField(max_length=255, null=True, verbose_name=b'Jabatan Pemohon', blank=True)),
                ('jenis_pemohon', models.ForeignKey(verbose_name=b'Jenis Pemohon', to='master.JenisPemohon')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Pemohon',
                'verbose_name_plural': 'Pemohon',
            },
            bases=('accounts.account',),
        ),
        migrations.AddField(
            model_name='dasarhukum',
            name='jenis_peraturan',
            field=models.ForeignKey(verbose_name=b'Jenis Peraturan', to='izin.JenisPeraturan'),
        ),
    ]
