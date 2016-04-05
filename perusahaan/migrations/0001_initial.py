# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('master', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AktaNotaris',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('no_akta', models.CharField(max_length=255, null=True, verbose_name=b'No Akta', blank=True)),
                ('tanggal_akta', models.DateField(null=True, verbose_name=b'Tanggal Akta', blank=True)),
                ('no_pengesahan', models.CharField(max_length=255, null=True, verbose_name=b'No Pengesahan', blank=True)),
                ('tanggal_pengesahan', models.DateField(verbose_name=b'Tanggal Pengesahan')),
                ('jenis_akta', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Akta', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Akta Notaris',
                'verbose_name_plural': 'Akta Notaris',
            },
        ),
        migrations.CreateModel(
            name='DataPimpinan',
            fields=[
                ('identitaspribadi_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='accounts.IdentitasPribadi')),
                ('tanggal_menduduki_jabatan', models.DateField(verbose_name=b'Tanggal Menduduki Jabatan')),
                ('jumlah_saham_dimiliki', models.DecimalField(verbose_name=b'Jumlah Saham Dimiliki', max_digits=5, decimal_places=2)),
                ('jumlah_saham_disetor', models.DecimalField(verbose_name=b'Jumlah Saham Disetor', max_digits=5, decimal_places=2)),
                ('kedudukan_diperusahaan_lain', models.CharField(max_length=255, verbose_name=b'Kedudukan Di Perusahaan Lain')),
                ('nama_perusahaan_lain', models.CharField(max_length=255, null=True, verbose_name=b'Nama Perusahaan Lain', blank=True)),
                ('alamat_perusahaan_lain', models.CharField(max_length=255, null=True, verbose_name=b'Alamat Perusahaan Lain', blank=True)),
                ('kode_pos_perusahaan_lain', models.IntegerField(null=True, verbose_name=b'Kode Pos Perusahaan Lain', blank=True)),
                ('telepon_perusahaan_lain', models.CharField(max_length=50, null=True, verbose_name=b'Telepon Perusahaan Lain', blank=True)),
                ('tanggal_menduduki_jabatan_perusahaan_lain', models.DateField(null=True, verbose_name=b' Tanggal Menduduki Jabatan Di Perusahaan Lain', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Data Pimpinan',
                'verbose_name_plural': 'Data Pimpinan',
            },
            bases=('accounts.identitaspribadi',),
        ),
        migrations.CreateModel(
            name='DataRincianPerusahaan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('omset_per_tahun', models.IntegerField(null=True, verbose_name=b'Omset Per Tahun', blank=True)),
                ('total_aset', models.IntegerField(verbose_name=b'Total Aset')),
                ('jumlah_karyawan_wni', models.IntegerField(verbose_name=b'Jumlah Karyawan WNI')),
                ('jumlah_karyawan_wna', models.IntegerField(verbose_name=b'Jumlah Karyawan WNA')),
                ('kapasitas_mesin_terpasang', models.IntegerField(verbose_name=b'Kapasitas Mesin Terpasang')),
                ('stuan_kapasitas_msin_terpasang', models.CharField(max_length=10, verbose_name=b'Satuan Kapasitas Mesin Terpasang')),
                ('kapasitas_produksi_pertahun', models.IntegerField(verbose_name=b'Kapasitas Produksi Per Tahun')),
                ('stuan_kapasitas_produksi', models.CharField(max_length=255, verbose_name=b'Satuan Kapasitas Produksi')),
                ('presentase_kandungan_komponen_produk_lokal', models.DecimalField(verbose_name=b'Presentase Kandungan Komponen Produk Lokal', max_digits=5, decimal_places=2)),
                ('presentase_kandungan_komponen_produk_import', models.DecimalField(verbose_name=b'Presentase Kandungan Komponen Produk Import', max_digits=5, decimal_places=2)),
                ('modal_dasar', models.IntegerField(verbose_name=b'Modal Dasar')),
                ('modal_disetor', models.IntegerField(verbose_name=b'Modal Disetor')),
                ('modal_ditempatkan', models.IntegerField(verbose_name=b'Modal Ditempatkan')),
                ('jumlah_saham', models.IntegerField(verbose_name=b'Jumlah Saham')),
                ('nilai_saham_per_lembar', models.IntegerField(verbose_name=b'Nilai Saham Per Lembar')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Data Rincian Perusahaan',
                'verbose_name_plural': 'Data Rincian Perusahaan',
            },
        ),
        migrations.CreateModel(
            name='JenisBadanUsaha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_badan_usaha', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Badan Usaha', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Badan Usaha',
                'verbose_name_plural': 'Jenis Badan Usaha',
            },
        ),
        migrations.CreateModel(
            name='JenisKedudukan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kedudukan', models.CharField(max_length=50, null=True, verbose_name=b'Kedudukan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Kedudukan',
                'verbose_name_plural': 'Jenis Kedudukan',
            },
        ),
        migrations.CreateModel(
            name='JenisKegiatanUsaha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_kegiatan_usaha', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Kegiatan Usaha', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Kegiatan Usaha',
                'verbose_name_plural': 'Jenis Kegiatan Usaha',
            },
        ),
        migrations.CreateModel(
            name='JenisKerjasama',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_kerjasama', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Kerjasama', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Kerjasama',
                'verbose_name_plural': 'Jenis Kerjasama',
            },
        ),
        migrations.CreateModel(
            name='JenisMesin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_mesin', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Mesin', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Mesin',
                'verbose_name_plural': 'Jenis Mesin',
            },
        ),
        migrations.CreateModel(
            name='JenisModalKoprasi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_modal_koprasi', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Modal Koprasi', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Modal Koprasi',
                'verbose_name_plural': 'Jenis Modal Koprasi',
            },
        ),
        migrations.CreateModel(
            name='JenisPenanamanModal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_penanaman_modal', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Penanaman Modal', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Penanaman Modal',
                'verbose_name_plural': 'Jenis Penanaman Modal',
            },
        ),
        migrations.CreateModel(
            name='JenisPengecer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_pengecer', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Pengecer', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Pengecer',
                'verbose_name_plural': 'Jenis Pengecer',
            },
        ),
        migrations.CreateModel(
            name='JenisPerusahaan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_perusahaan', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Perusahaan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Perusahaan',
                'verbose_name_plural': 'Jenis Perusahaan',
            },
        ),
        migrations.CreateModel(
            name='KBLI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kode_kbli', models.IntegerField(null=True, verbose_name=b'Kode KBLI', blank=True)),
                ('nama_kbli', models.CharField(max_length=255, null=True, verbose_name=b'Nama KBLI', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'KBLI',
                'verbose_name_plural': 'KBLI',
            },
        ),
        migrations.CreateModel(
            name='KegiatanUsaha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kegiatan_usaha', models.CharField(max_length=255, null=True, verbose_name=b'Kegiatan Usaha', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Kegiatan Usaha',
                'verbose_name_plural': 'Kegiatan Usaha',
            },
        ),
        migrations.CreateModel(
            name='Kelembagaan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_kelembagaan', models.CharField(max_length=255, null=True, verbose_name=b'Nama Kelembagaan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Kelembagaan',
                'verbose_name_plural': 'Kelembagaan',
            },
        ),
        migrations.CreateModel(
            name='LokasiUnitProduksi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alamat', models.CharField(max_length=255, verbose_name=b'Alamat')),
                ('desa', models.ForeignKey(verbose_name=b'Desa', to='master.Desa')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Lokasi Unit Perusahaan',
                'verbose_name_plural': 'Lokasi Unit Perusahaan',
            },
        ),
        migrations.CreateModel(
            name='MesinHuller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mesin_huller', models.CharField(max_length=255, null=True, verbose_name=b'Mesin Huller', blank=True)),
                ('jenis', models.ForeignKey(verbose_name=b'Jenis Mesin', to='perusahaan.JenisMesin')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Mesin Huller',
                'verbose_name_plural': 'Mesin Huller',
            },
        ),
        migrations.CreateModel(
            name='MesinPerusahaan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipe', models.CharField(max_length=255, verbose_name=b'Type')),
                ('PK', models.CharField(max_length=255, verbose_name=b'PK')),
                ('kapasitas', models.IntegerField(verbose_name=b'Kapasitas')),
                ('merk', models.CharField(max_length=255, verbose_name=b'Merk')),
                ('jumlah_unit', models.CharField(max_length=255, verbose_name=b'Jumlah Unit')),
                ('mesin', models.ForeignKey(verbose_name=b'Mesin Huller', to='perusahaan.MesinHuller')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': ' Mesin Perusahaan',
                'verbose_name_plural': 'Mesin Perusahaan',
            },
        ),
        migrations.CreateModel(
            name='ModalKoprasi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modal_koprasi', models.CharField(max_length=255, null=True, verbose_name=b'Modal Koprasi', blank=True)),
                ('jenis_modal', models.ForeignKey(verbose_name=b'Jenis Modal Koprasi', to='perusahaan.JenisModalKoprasi')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Modal Koprasi',
                'verbose_name_plural': 'Modal Koprasi',
            },
        ),
        migrations.CreateModel(
            name='NilaiModal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nilai', models.IntegerField(verbose_name=b'Modal Koprasi')),
                ('modal', models.ForeignKey(verbose_name=b'Modal Koprasi', to='perusahaan.ModalKoprasi')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Nilai Modal',
                'verbose_name_plural': 'Nilai Modal',
            },
        ),
        migrations.CreateModel(
            name='PemegangSahamLain',
            fields=[
                ('identitaspribadi_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='accounts.IdentitasPribadi')),
                ('npwp', models.IntegerField(null=True, verbose_name=b'NPWP', blank=True)),
                ('jumlah_saham_dimiliki', models.IntegerField(verbose_name=b'Jumlah Saham Dimiliki')),
                ('jumlah_modal_disetor', models.IntegerField(verbose_name=b'Jumlah Modal Disetor')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Pemegang Saham Lain',
                'verbose_name_plural': 'Pemegang Saham Lain',
            },
            bases=('accounts.identitaspribadi',),
        ),
        migrations.CreateModel(
            name='Perusahaan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_perusahaan', models.CharField(max_length=100, verbose_name=b'Nama Perusahaan')),
                ('alamat_perusahaan', models.CharField(max_length=255, null=True, verbose_name=b'Alamat Perusahaan', blank=True)),
                ('lt', models.CharField(max_length=100, null=True, verbose_name=b'Latitute')),
                ('lg', models.CharField(max_length=100, null=True, verbose_name=b'Longitute')),
                ('kode_pos', models.IntegerField(verbose_name=b'Kode Pos')),
                ('telepon', models.CharField(max_length=50, null=True, verbose_name=b'Telepon', blank=True)),
                ('fax', models.CharField(max_length=20, verbose_name=b'Fax')),
                ('email', models.EmailField(max_length=50, null=True, verbose_name=b'E-mail', blank=True)),
                ('nama_kelompok_perusahaan', models.CharField(max_length=100, verbose_name=b'Nama Kelompok Perusahaan')),
                ('nasabah_utama_bank1', models.CharField(max_length=255, verbose_name=b'Nasabah Utama Bank 1')),
                ('nasabah_utama_bank2', models.CharField(max_length=255, verbose_name=b'Nasabah Utama Bank 2')),
                ('jumlah_bank', models.IntegerField(verbose_name=b'Jumlah Bank')),
                ('npwp', models.IntegerField(null=True, verbose_name=b'NPWP', blank=True)),
                ('tanggal_pendirian', models.DateField(verbose_name=b'Tanggal Pendirian')),
                ('tanggal_mulai_kegiatan', models.DateField(verbose_name=b'Tanggal Mulai Kegiatan')),
                ('merk_dagang', models.CharField(max_length=255, verbose_name=b'Merk Dagang')),
                ('pemegang_hak_paten', models.CharField(max_length=255, verbose_name=b'Pemegang Hak Paten')),
                ('pemegang_hak_cipta', models.CharField(max_length=255, verbose_name=b'Pemegang Hak Cipta')),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name=b'Status Data', choices=[(1, b'Active'), (2, b'Inactive'), (3, b'Blocked'), (4, b'Submitted'), (5, b'Archive')])),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('badan_usaha', models.ForeignKey(verbose_name=b'Jenis Badan Usaha', blank=True, to='perusahaan.JenisBadanUsaha', null=True)),
                ('jenis_perusahaan', models.ForeignKey(verbose_name=b'Jenis Perusahaan', blank=True, to='perusahaan.JenisPerusahaan', null=True)),
                ('kbli', models.ForeignKey(verbose_name=b'KBLI', blank=True, to='perusahaan.KBLI', null=True)),
                ('kerjasama', models.ForeignKey(verbose_name=b'Jenis Kerjasama', blank=True, to='perusahaan.JenisKerjasama', null=True)),
                ('penanaman_modal', models.ForeignKey(verbose_name=b'Jenis Penanaman Modal', blank=True, to='perusahaan.JenisPenanamanModal', null=True)),
                ('perusahaan_induk', models.ForeignKey(blank=True, to='perusahaan.Perusahaan', null=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Perusahaan',
                'verbose_name_plural': 'Perusahaan',
            },
        ),
        migrations.CreateModel(
            name='ProdukUtama',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('barang_jasa_utama', models.CharField(max_length=255, verbose_name=b'Barang Jasa Utama')),
                ('kelembagaan', models.ForeignKey(verbose_name=b'Kelembagaan', to='perusahaan.Kelembagaan')),
                ('perusahaan', models.ForeignKey(verbose_name=b'Perusahaan', to='perusahaan.Perusahaan')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Produk Utama',
                'verbose_name_plural': 'Produk Utama',
            },
        ),
        migrations.CreateModel(
            name='StatusPerusahaan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_perusahaan', models.CharField(max_length=255, null=True, verbose_name=b'Status Perusahaan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Status Perusahaan',
                'verbose_name_plural': 'Status Perusahaan',
            },
        ),
        migrations.AddField(
            model_name='perusahaan',
            name='status_perusahaan',
            field=models.ForeignKey(verbose_name=b'Status Perusahaan', blank=True, to='perusahaan.StatusPerusahaan', null=True),
        ),
        migrations.AddField(
            model_name='pemegangsahamlain',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', to='perusahaan.Perusahaan'),
        ),
        migrations.AddField(
            model_name='nilaimodal',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', to='perusahaan.Perusahaan'),
        ),
        migrations.AddField(
            model_name='mesinperusahaan',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', to='perusahaan.Perusahaan'),
        ),
        migrations.AddField(
            model_name='lokasiunitproduksi',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', to='perusahaan.Perusahaan'),
        ),
        migrations.AddField(
            model_name='datarincianperusahaan',
            name='jenis_kegiatan',
            field=models.ForeignKey(verbose_name=b'Jenis Kegiatan Usaha', blank=True, to='perusahaan.JenisKegiatanUsaha', null=True),
        ),
        migrations.AddField(
            model_name='datarincianperusahaan',
            name='kegiatan_usaha',
            field=models.ForeignKey(verbose_name=b'Kegiatan Usaha', blank=True, to='perusahaan.KegiatanUsaha', null=True),
        ),
        migrations.AddField(
            model_name='datarincianperusahaan',
            name='pengecer',
            field=models.ForeignKey(verbose_name=b'Jenis Pengecer', blank=True, to='perusahaan.JenisPengecer', null=True),
        ),
        migrations.AddField(
            model_name='datarincianperusahaan',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', to='perusahaan.Perusahaan'),
        ),
        migrations.AddField(
            model_name='datapimpinan',
            name='kedudukan',
            field=models.ForeignKey(verbose_name=b'Jenis Kedudukan', to='perusahaan.JenisKedudukan'),
        ),
        migrations.AddField(
            model_name='datapimpinan',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', to='perusahaan.Perusahaan'),
        ),
        migrations.AddField(
            model_name='aktanotaris',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', to='perusahaan.Perusahaan'),
        ),
    ]
