from django.conf import settings
from django.conf.urls import patterns, url, include

import views

urlpatterns = [
	url(r'^apotek/save-izin-apotek/$', views.save_izin_apotek, name='izin_dinkes__save_izin_apotek'),
	url(r'^apotek/upload-berkas/$', views.upload_berkas, name='izin_dinkes__upload_berkas'),
	url(r'^apotek/upload-berkas/save/$', views.apotek_upload_dokumen_cookie, name='izin_dinkes__upload_berkas_save'),

	############### Izin Toko Obat ###############
	url(r'^toko-obat/save-izin-toko-obat/$', views.save_izin_toko_obat, name='izin_dinkes__save_izin_toko_obat'),
	url(r'^toko-obat/load-berkas/(?P<id_pengajuan>[0-9]+)$', views.load_berkas_toko_obat, name='izin_dinkes__load_berkas_toko_obat'),
	url(r'^toko-obat/validasi-berkas/$', views.validasi_berkas_toko_obat, name='izin_dinkes__validasi_berkas_toko_obat'),
	url(r'^toko-obat/upload-berkas/$', views.upload_berkas_toko_obat, name='izin_dinkes__upload_berkas_toko_obat'),
	############### end Izin Toko Obat ###########
]