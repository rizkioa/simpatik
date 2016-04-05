# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perusahaan', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CeklisSyaratIzin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cek', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Ceklis Syarat Izin',
                'verbose_name_plural': 'Ceklis Syarat Izin',
            },
        ),
        migrations.CreateModel(
            name='DasarHukum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instansi', models.CharField(max_length=100, null=True, verbose_name=b'Instansi', blank=True)),
                ('nomor', models.CharField(max_length=100, null=True, verbose_name=b'Nomor', blank=True)),
                ('tentang', models.CharField(max_length=255, null=True, verbose_name=b'Tentang', blank=True)),
                ('keterangan', models.CharField(max_length=255, verbose_name=b'Keterangan')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Dasar Hukum',
                'verbose_name_plural': 'Dasar Hukum',
            },
        ),
        migrations.CreateModel(
            name='DataPerubahan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tabel_asal', models.CharField(max_length=255, null=True, verbose_name=b'Tabel Asal', blank=True)),
                ('nama_field', models.CharField(max_length=255, null=True, verbose_name=b'Nama Field', blank=True)),
                ('isi_field_lama', models.CharField(max_length=255, null=True, verbose_name=b'Isi Field Lama', blank=True)),
                ('created_at', models.DateTimeField(editable=False)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Data Perubahan',
                'verbose_name_plural': 'Data Perubahan',
            },
        ),
        migrations.CreateModel(
            name='DataReklame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('judul_reklame', models.CharField(max_length=255, null=True, verbose_name=b'Judul Reklame', blank=True)),
                ('panjang', models.DecimalField(verbose_name=b'Panjang', max_digits=5, decimal_places=2)),
                ('lebar', models.DecimalField(verbose_name=b'Lebar', max_digits=5, decimal_places=2)),
                ('sisi', models.DecimalField(null=True, verbose_name=b'Sisi', max_digits=5, decimal_places=2, blank=True)),
                ('lama_pemasangan', models.IntegerField(null=True, verbose_name=b'Lama Pemasangan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Data Reklame',
                'verbose_name_plural': 'Data Reklame',
            },
        ),
        migrations.CreateModel(
            name='DetilHo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('perkiraan_modal', models.DecimalField(verbose_name=b'Perkiraan Modal', max_digits=10, decimal_places=2)),
                ('keperluan', models.CharField(max_length=255, verbose_name=b'Keperluan')),
                ('alamat', models.CharField(max_length=255, verbose_name=b'Alamat')),
                ('bahan_baku_dan_penolong', models.CharField(max_length=255, verbose_name=b'Bahan Baku Dan Penolong')),
                ('proses_produksi', models.CharField(max_length=255, verbose_name=b'Proses Produksi')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Detil HO',
                'verbose_name_plural': 'Detil HO',
            },
        ),
        migrations.CreateModel(
            name='DetilIMBGedung',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('luas_bangunan', models.DecimalField(verbose_name=b'Luas Bangunan', max_digits=5, decimal_places=2)),
                ('unit', models.IntegerField(verbose_name=b'Unit')),
                ('luas_tanah', models.DecimalField(verbose_name=b'Luas Tanah', max_digits=5, decimal_places=2)),
                ('no_surat_tanah', models.CharField(max_length=255, verbose_name=b'No Surat Tanah')),
                ('tanggal_surat_tanah', models.DateField()),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Detil IMB Gedung',
                'verbose_name_plural': 'Detil IMB Gedung',
            },
        ),
        migrations.CreateModel(
            name='DetilIMBPapanReklame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_papan_reklame', models.CharField(max_length=255, verbose_name=b'Jenis Papan Reklame')),
                ('lebar', models.DecimalField(verbose_name=b'Lebar', max_digits=5, decimal_places=2)),
                ('tinggi', models.DecimalField(verbose_name=b'Tinggi', max_digits=5, decimal_places=2)),
                ('lokasi_pasang', models.CharField(max_length=255, null=True, verbose_name=b'Lokasi Pasang', blank=True)),
                ('batas_utara', models.CharField(max_length=255, null=True, verbose_name=b'Batas Utara', blank=True)),
                ('batas_timur', models.CharField(max_length=255, null=True, verbose_name=b'Batas Timur', blank=True)),
                ('batas_selatan', models.CharField(max_length=255, null=True, verbose_name=b'Batas Selatan', blank=True)),
                ('batas_barat', models.CharField(max_length=255, null=True, verbose_name=b'Bats Barat', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Detil IMB Papan Reklame',
                'verbose_name_plural': 'Detil IMB Papan Reklame',
            },
        ),
        migrations.CreateModel(
            name='Izin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pendaftaran', models.SmallIntegerField(verbose_name=b'Pendaftaran')),
                ('pembaharuan', models.IntegerField(verbose_name=b'Pembaharuan')),
                ('status', models.PositiveSmallIntegerField(default=1, verbose_name=b'Status Data', choices=[(1, b'Active'), (2, b'Inactive'), (3, b'Blocked'), (4, b'Submitted'), (5, b'Archive')])),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('detil_papan_reklame', models.ForeignKey(verbose_name=b'Detil IMB Papan Reklame', to='izin.DetilIMBPapanReklame')),
                ('izin_induk', models.ForeignKey(blank=True, to='izin.Izin', null=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Izin',
                'verbose_name_plural': 'Izin',
            },
        ),
        migrations.CreateModel(
            name='JenisBangunan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_bangunan', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Bangunan', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Bangunan',
                'verbose_name_plural': 'Jenis Bangunan',
            },
        ),
        migrations.CreateModel(
            name='JenisGangguan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_gangguan', models.CharField(max_length=255, verbose_name=b'Jenis Gangguan')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Gangguan',
                'verbose_name_plural': 'Jenis Gangguan',
            },
        ),
        migrations.CreateModel(
            name='JenisIzin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_izin', models.CharField(max_length=100, null=True, verbose_name=b'Nama Izin', blank=True)),
                ('jenis_izin', models.CharField(max_length=20, null=True, verbose_name=b'Jenis Izin', blank=True)),
                ('keterangan', models.CharField(max_length=255, verbose_name=b'Keterangan')),
                ('dasar_hukum', models.ManyToManyField(to='izin.DasarHukum', verbose_name=b'Dasar Hukum')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Izin',
                'verbose_name_plural': 'Jenis Izin',
            },
        ),
        migrations.CreateModel(
            name='JenisKegiatanPembangunan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_kegiatan_pembangunan', models.CharField(max_length=255, verbose_name=b'Jenis Kegiatan Pembangunan')),
                ('detil_jenis_kegiatan', models.CharField(max_length=255, null=True, verbose_name=b'Detil Jenis Kegiatan', blank=True)),
                ('nilai', models.IntegerField(verbose_name=b'Nilai')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Kegiatan Pembangunan',
                'verbose_name_plural': 'Jenis Kegiatan pembangunan',
            },
        ),
        migrations.CreateModel(
            name='jenisLokasiUsaha',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_lokasi_usaha', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Lokasi Usaha', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Lokasi Usaha',
                'verbose_name_plural': 'Jenis Lokasi Usaha',
            },
        ),
        migrations.CreateModel(
            name='JenisPemohon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_pemohon', models.CharField(max_length=255, null=True, verbose_name=b'Jenis Pemohon', blank=True)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Pemohon',
                'verbose_name_plural': 'Jenis Pemohon',
            },
        ),
        migrations.CreateModel(
            name='JenisPeraturan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_peraturan', models.CharField(max_length=100, null=True, verbose_name=b'Jenis Peraturan', blank=True)),
                ('keterangan', models.CharField(max_length=255, verbose_name=b'Keterangan')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Peraturan',
                'verbose_name_plural': 'Jenis Peraturan',
            },
        ),
        migrations.CreateModel(
            name='JenisPermohonanIzin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_permohonan_izin', models.CharField(max_length=255, verbose_name=b'Jenis Permohonan Izin')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Permohonan Izin',
                'verbose_name_plural': 'Jenis Permohonan Izin',
            },
        ),
        migrations.CreateModel(
            name='JenisReklame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_reklame', models.CharField(max_length=255, verbose_name=b'Jenis Reklame')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Reklame',
                'verbose_name_plural': 'Jenis Reklame',
            },
        ),
        migrations.CreateModel(
            name='JenisTanah',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jenis_tanah', models.CharField(max_length=255, verbose_name=b'Jenis Tanah')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Jenis Tanah',
                'verbose_name_plural': 'Jenis Tanah',
            },
        ),
        migrations.CreateModel(
            name='KekayaanDanSaham',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kekayaan_bersih', models.DecimalField(null=True, verbose_name=b'Kekayaan Bersih', max_digits=10, decimal_places=2)),
                ('total_nilai_saham', models.DecimalField(null=True, verbose_name=b'Total Nilai Saham', max_digits=5, decimal_places=2, blank=True)),
                ('presentase_saham_nasional', models.DecimalField(null=True, verbose_name=b'Presentase Saham Nasional', max_digits=5, decimal_places=2, blank=True)),
                ('presentase_saham_asing', models.DecimalField(null=True, verbose_name=b'Presentase Saham Asing', max_digits=5, decimal_places=2, blank=True)),
                ('izin', models.ForeignKey(verbose_name=b'Izin', to='izin.Izin')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Kekayaan Dan Saham',
                'verbose_name_plural': 'Kekayaan Dan Saham',
            },
        ),
        migrations.CreateModel(
            name='KelompokJenisIzin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kelompok_jenis_izin', models.CharField(max_length=100, null=True, verbose_name=b'Kelompok Jenis Izin', blank=True)),
                ('biaya', models.DecimalField(null=True, verbose_name=b'Biaya', max_digits=10, decimal_places=2, blank=True)),
                ('standart_waktu', models.DateTimeField()),
                ('keterangan', models.CharField(max_length=255, verbose_name=b'Keterangan')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Kelompok Jenis Izin',
                'verbose_name_plural': 'Kelompok Jenis Izin',
            },
        ),
        migrations.CreateModel(
            name='KepemilikkanTanah',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kepemilikan_tanah', models.CharField(max_length=255, verbose_name=b'Kepemilikan Tanah')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Kepemilikan Tanah',
                'verbose_name_plural': 'Kepemilikan Tanah',
            },
        ),
        migrations.CreateModel(
            name='ParameterBangunan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parameter', models.CharField(max_length=255, verbose_name=b'Parameter')),
                ('detil_parameter', models.CharField(max_length=255, null=True, verbose_name=b'Detil Parameter', blank=True)),
                ('nilai', models.IntegerField(verbose_name=b'Nilai')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Parameter Bangunan',
                'verbose_name_plural': 'Parameter Bangunan',
            },
        ),
        migrations.CreateModel(
            name='Pemohon',
            fields=[
                ('account_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('jabatan_pemohon', models.CharField(max_length=255, null=True, verbose_name=b'Jabatan Pemohon', blank=True)),
                ('jenis_pemohon', models.ForeignKey(verbose_name=b'Jenis Pemohon', to='izin.JenisPemohon')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Pemohon',
                'verbose_name_plural': 'Pemohon',
            },
            bases=('accounts.account',),
        ),
        migrations.CreateModel(
            name='Prosedur',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prosedur', models.CharField(max_length=255, null=True, verbose_name=b'Prosedur', blank=True)),
                ('lama', models.DateTimeField()),
                ('keterangan', models.CharField(max_length=255, verbose_name=b'Keterangan')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Prosedur',
                'verbose_name_plural': 'Prosedur',
            },
        ),
        migrations.CreateModel(
            name='StatusHakTanah',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hak_tanah', models.CharField(max_length=255, verbose_name=b'Hak Tanah')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Status Hak Tanah',
                'verbose_name_plural': 'Status Hak Tanah',
            },
        ),
        migrations.CreateModel(
            name='StatusVerifikasi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cek_status', models.BooleanField()),
                ('tanggal_verifikasi', models.DateField()),
                ('keterangan', models.CharField(max_length=255, null=True, verbose_name=b'Keterangan', blank=True)),
                ('account', models.ForeignKey(verbose_name=b'User', to=settings.AUTH_USER_MODEL)),
                ('izin', models.ForeignKey(verbose_name=b'Izin', to='izin.Izin')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Status Verifikasi',
                'verbose_name_plural': 'Status Verifikasi',
            },
        ),
        migrations.CreateModel(
            name='Syarat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('syarat', models.CharField(max_length=255, null=True, verbose_name=b'Syarat', blank=True)),
                ('keterangan', models.CharField(max_length=255, verbose_name=b'Keterangan')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Syarat',
                'verbose_name_plural': 'Syarat',
            },
        ),
        migrations.CreateModel(
            name='VerivikasiIzin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nama_verifikasi', models.CharField(max_length=255, verbose_name=b'Nama Verifikasi')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name': 'Verifikasi Izin',
                'verbose_name_plural': 'Verifikasi Izin',
            },
        ),
        migrations.AddField(
            model_name='statusverifikasi',
            name='nama_verifikasi',
            field=models.ForeignKey(verbose_name=b'Verifikasi Izin', to='izin.VerivikasiIzin'),
        ),
        migrations.AddField(
            model_name='jenisizin',
            name='kelompok_izin',
            field=models.ForeignKey(verbose_name=b'Kelompok Jenis Izin', to='izin.KelompokJenisIzin'),
        ),
        migrations.AddField(
            model_name='izin',
            name='jenis_gangguan',
            field=models.ManyToManyField(to='izin.JenisGangguan', verbose_name=b'Jenis Gangguan'),
        ),
        migrations.AddField(
            model_name='izin',
            name='jenis_kegiatan_pembangunan',
            field=models.ManyToManyField(to='izin.JenisKegiatanPembangunan', verbose_name=b'Jenis Kegiatan Pembangunan'),
        ),
        migrations.AddField(
            model_name='izin',
            name='jenis_permohonan',
            field=models.ForeignKey(verbose_name=b'Jenis Permohonan Izin', to='izin.JenisPermohonanIzin'),
        ),
        migrations.AddField(
            model_name='izin',
            name='kelompok_jenis_izin',
            field=models.ForeignKey(verbose_name=b'Kelompok Jenis Izin', to='izin.KelompokJenisIzin'),
        ),
        migrations.AddField(
            model_name='izin',
            name='parameter_bgunan',
            field=models.ManyToManyField(to='izin.ParameterBangunan', verbose_name=b'Parameter'),
        ),
        migrations.AddField(
            model_name='izin',
            name='pemohon',
            field=models.ForeignKey(related_name='Pemohon', to='izin.Pemohon'),
        ),
        migrations.AddField(
            model_name='izin',
            name='perusahaan',
            field=models.ForeignKey(verbose_name=b'Perusahaan', blank=True, to='perusahaan.Perusahaan', null=True),
        ),
        migrations.AddField(
            model_name='izin',
            name='user',
            field=models.ForeignKey(related_name='User', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='detilimbgedung',
            name='izin',
            field=models.ForeignKey(verbose_name=b'Izin', to='izin.Izin'),
        ),
        migrations.AddField(
            model_name='detilimbgedung',
            name='jenis_tanah',
            field=models.ForeignKey(verbose_name=b'JenisTanah', to='izin.JenisTanah'),
        ),
        migrations.AddField(
            model_name='detilimbgedung',
            name='kepemilikan_tanah',
            field=models.ForeignKey(verbose_name=b'Kepemilikan Tanah', to='izin.KepemilikkanTanah'),
        ),
        migrations.AddField(
            model_name='detilimbgedung',
            name='status_tanah',
            field=models.ForeignKey(verbose_name=b'Status Hak Tanah', to='izin.StatusHakTanah'),
        ),
        migrations.AddField(
            model_name='detilho',
            name='izin',
            field=models.ForeignKey(verbose_name=b'Izin', to='izin.Izin'),
        ),
        migrations.AddField(
            model_name='detilho',
            name='jenis_bangunan',
            field=models.ForeignKey(verbose_name=b'Jenis Bangunan', to='izin.JenisBangunan'),
        ),
        migrations.AddField(
            model_name='detilho',
            name='jenis_lokasi',
            field=models.ForeignKey(verbose_name=b'Jenis Lokasi Usaha', to='izin.jenisLokasiUsaha'),
        ),
        migrations.AddField(
            model_name='datareklame',
            name='izin',
            field=models.ForeignKey(verbose_name=b'Izin', to='izin.Izin'),
        ),
        migrations.AddField(
            model_name='datareklame',
            name='jenis_reklame',
            field=models.ForeignKey(verbose_name=b'Jenis Reklame', to='izin.JenisReklame'),
        ),
        migrations.AddField(
            model_name='dasarhukum',
            name='jenis_peraturan',
            field=models.ForeignKey(verbose_name=b'Jenis Peraturan', to='izin.JenisPeraturan'),
        ),
        migrations.AddField(
            model_name='ceklissyaratizin',
            name='izin',
            field=models.ForeignKey(verbose_name=b'Izin', to='izin.Izin'),
        ),
        migrations.AddField(
            model_name='ceklissyaratizin',
            name='syarat',
            field=models.ForeignKey(verbose_name=b'Syarat', to='izin.Syarat'),
        ),
    ]
