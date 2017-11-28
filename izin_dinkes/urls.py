from django.conf import settings
from django.conf.urls import patterns, url, include

import views

urlpatterns = [
	url(r'^apotek/save-izin-apotek/$', views.save_izin_apotek, name='izin_dinkes__save_izin_apotek'),
	url(r'^apotek/upload-berkas/$', views.upload_berkas, name='izin_dinkes__upload_berkas'),
	url(r'^apotek/upload-berkas/save/$', views.apotek_upload_dokumen_cookie, name='izin_dinkes__upload_berkas_save'),
    url(r'^apotek/load-berkas/ajax/(?P<id_pengajuan>[0-9]+)$', views.ajax_load_berkas_apotek, name='izin_dinkes__ajax_load_berkas_apotek'),
    url(r'^apotek/load-konfirmasi-apotek/ajax/(?P<id_pengajuan>[0-9]+)$', views.load_konfirmasi_apotek, name='izin_dinkes__load_konfirmasi_apotek'),
    url(r'^apotek/validasi-berkas/$', views.validasi_berkas_apotek, name='izin_dinkes__validasi_berkas_apotek'),
    url(r'^apotek/apotek-done/$', views.apotek_done, name='izin_dinkes__apotek_done'),

	############### Izin Toko Obat ###############
	url(r'^toko-obat/save-izin-toko-obat/$', views.save_izin_toko_obat, name='izin_dinkes__save_izin_toko_obat'),
	url(r'^toko-obat/load-berkas/(?P<id_pengajuan>[0-9]+)$', views.load_berkas_toko_obat, name='izin_dinkes__load_berkas_toko_obat'),
	url(r'^toko-obat/validasi-berkas/$', views.validasi_berkas_toko_obat, name='izin_dinkes__validasi_berkas_toko_obat'),
	url(r'^toko-obat/upload-berkas/$', views.upload_berkas_toko_obat, name='izin_dinkes__upload_berkas_toko_obat'),
	############### end Izin Toko Obat ###########

	############### Izin Lab ###############
	url(r'^laboratorium/save-izin-laboratorium/$', views.save_izin_laboratorium, name='izin_dinkes__save_izin_laboratorium'),

	url(r'^laboratorium/save-peralatan-laboratorium/$', views.save_peralatan_lab, name='izin_dinkes__save_peralatan_lab'),
	url(r'^laboratorium/load-peralatan-laboratorium/(?P<id_pengajuan>[0-9]+)$', views.load_peralatan_lab, name='izin_dinkes__load_peralatan_lab'),
	url(r'^laboratorium/load-edit-peralatan-laboratorium/(?P<id_peralatan_lab>[0-9]+)$', views.load_edit_peralatan_lab, name='izin_dinkes__load_edit_peralatan_lab'),
	url(r'^laboratorium/delete-peralatan-laboratorium/(?P<id_peralatan_lab>[0-9]+)$', views.delete_peralatan_lab, name='izin_dinkes__delete_peralatan_lab'),
	url(r'^laboratorium/peralatan-next/$', views.next_tab_peralatan_cookie, name='izin_dinkes__next_tab_peralatan_cookie'),

	url(r'^laboratorium/save-bangunan-laboratorium/$', views.save_bangunan_lab, name='izin_dinkes__save_bangunan_lab'),
	url(r'^laboratorium/load-bangunan-laboratorium/(?P<id_pengajuan>[0-9]+)$', views.load_bangunan_lab, name='izin_dinkes__load_bangunan_lab'),
	url(r'^laboratorium/load-edit-bangunan-laboratorium/(?P<id_bangunan_lab>[0-9]+)$', views.load_edit_bangunan_lab, name='izin_dinkes__load_edit_bangunan_lab'),
	url(r'^laboratorium/delete-bangunan-laboratorium/(?P<id_bangunan_lab>[0-9]+)$', views.delete_bangunan_lab, name='izin_dinkes__delete_bangunan_lab'),
	url(r'^laboratorium/bangunan-next/$', views.next_tab_bangunan_cookie, name='izin_dinkes__next_tab_bangunan_cookie'),

	url(r'^laboratorium/upload-berkas-lab/$', views.upload_berkas_laboratorium, name='izin_dinkes__upload_berkas_laboratorium'),
	url(r'^laboratorium/upload-berkas-lab/save/$', views.laboratorium_upload_dokumen_cookie, name='izin_dinkes__upload_berkas_laboratorium_save'),
    url(r'^laboratorium/load-berkas/ajax/(?P<id_pengajuan>[0-9]+)$', views.ajax_load_berkas_laboratorium, name='izin_dinkes__ajax_load_berkas_laboratorium'),
    url(r'^laboratorium/load-konfirmasi-laboratorium/ajax/(?P<id_pengajuan>[0-9]+)$', views.load_konfirmasi_laboratorium, name='izin_dinkes__load_konfirmasi_laboratorium'),
    url(r'^laboratorium/laboratorium-done/$', views.laboratorium_done, name='izin_dinkes__laboratorium_done'),

	############### end Izin Lab ##########
]