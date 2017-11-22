from django.conf import settings
from django.conf.urls import patterns, url, include

import views

urlpatterns = [
	url(r'^apotek/save-izin-apotek/$', views.save_izin_apotek, name='izin_dinkes__save_izin_apotek'),
	url(r'^apotek/upload-berkas/$', views.upload_berkas, name='izin_dinkes__upload_berkas'),
	url(r'^apotek/upload-berkas/save/$', views.apotek_upload_dokumen_cookie, name='izin_dinkes__upload_berkas_save'),
    url(r'^apotek/load-berkas/ajax/(?P<id_pengajuan>[0-9]+)$', views.ajax_load_berkas_apotek, name='izin_dinkes__ajax_load_berkas_apotek'),
    url(r'^apotek/load-konfirmasi-apotek/ajax/(?P<id_pengajuan>[0-9]+)$', views.load_konfirmasi_apotek, name='izin_dinkes__load_konfirmasi_apotek'),
    url(r'^apotek/apotek-done/$', views.apotek_done, name='izin_dinkes__apotek_done'),

	url(r'^save-izin-toko-obat/$', views.save_izin_toko_obat, name='izin_dinkes__save_izin_toko_obat'),
	
]