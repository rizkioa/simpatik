from django.conf import settings
from django.conf.urls import patterns, url, include
import views
import views_dinkes

urlpatterns = [
	url(r'^apotek/save-izin-apotek/$', views.save_izin_apotek, name='izin_dinkes__save_izin_apotek'),
	url(r'^apotek/load-izin-apotek/(?P<id_pengajuan>[0-9]+)$', views.load_izin_apotek, name='izin_dinkes__load_izin_apotek'),
	url(r'^apotek/upload-berkas/$', views.upload_berkas, name='izin_dinkes__upload_berkas'),
	url(r'^apotek/upload-berkas/save/$', views.apotek_upload_dokumen_cookie, name='izin_dinkes__upload_berkas_save'),
    url(r'^apotek/load-berkas/ajax/(?P<id_pengajuan>[0-9]+)$', views.ajax_load_berkas_apotek, name='izin_dinkes__ajax_load_berkas_apotek'),
    url(r'^apotek/load-konfirmasi-apotek/ajax/(?P<id_pengajuan>[0-9]+)$', views.load_konfirmasi_apotek, name='izin_dinkes__load_konfirmasi_apotek'),
    # url(r'^apotek/validasi-berkas/$', views.validasi_berkas_apotek, name='izin_dinkes__validasi_berkas_apotek'),
    url(r'^apotek/apotek-done/$', views.apotek_done, name='izin_dinkes__apotek_done'),

	############### Izin Toko Obat ###############
	url(r'^toko-obat/save-izin-toko-obat/$', views.save_izin_toko_obat, name='izin_dinkes__save_izin_toko_obat'),
	url(r'^toko-obat/load-berkas/(?P<id_pengajuan>[0-9]+)$', views.load_berkas_toko_obat, name='izin_dinkes__load_berkas_toko_obat'),
	url(r'^toko-obat/load-konfirmasi/(?P<id_pengajuan>[0-9]+)$', views.load_konfirmasi_toko_obat, name='izin_dinkes__load_konfirmasi_toko_obat'),
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

	############### Izin penutupan apotek ##########
	url(r'^penutupan-apotek/save-izin-penutupan-apotek/$', views.save_izin_penutupan_apotek, name='izin_dinkes__save_izin_penutupan_apotek'),
	url(r'^penutupan-apotek/load-izin-penutupan-apotek/(?P<id_pengajuan>[0-9]+)$', views.load_izin_penutupan_apotek, name='izin_dinkes__load_izin_penutupan_apotek'),

	url(r'^penutupan-apotek/upload-berkas-penutupan-apotek/$', views.upload_berkas_penutupan_apotek, name='izin_dinkes__upload_berkas_penutupan_apotek'),
	url(r'^penutupan-apotek/upload-berkas-penutupan-apotek/save/$', views.penutupan_apotek_upload_dokumen_cookie, name='izin_dinkes__upload_berkas_penutupan_apotek_save'),
    url(r'^penutupan-apotek/load-berkas/ajax/(?P<id_pengajuan>[0-9]+)$', views.ajax_load_berkas_penutupan_apotek, name='izin_dinkes__ajax_load_berkas_penutupan_apotek'),

    url(r'^penutupan-apotek/save-pengunduran-apoteker/$', views.save_pengunduran_apoteker, name='izin_dinkes__save_pengunduran'),
	url(r'^penutupan-apotek/load-pengunduran-apoteker/(?P<id_pengajuan>[0-9]+)$', views.load_pengunduran_apoteker, name='izin_dinkes__load_pengunduran'),
	url(r'^penutupan-apotek/load-edit-pengunduran-apoteker/(?P<id_pengunduran>[0-9]+)$', views.load_edit_pengunduran_apoteker, name='izin_dinkes__load_edit_pengunduran'),
	url(r'^penutupan-apotek/delete-pengunduran-apoteker/(?P<id_pengunduran>[0-9]+)$', views.delete_pengunduran_apoteker, name='izin_dinkes__delete_pengunduran'),
	url(r'^penutupan-apotek/pengunduran-apoteker-next/$', views.next_tab_penutupan_cookie, name='izin_dinkes__next_tab_penutupan_cookie'),

    url(r'^penutupan-apotek/load-konfirmasi-penutupan-apotek/ajax/(?P<id_pengajuan>[0-9]+)$', views.load_konfirmasi_penutupan_apotek, name='izin_dinkes__load_konfirmasi_penutupan_apotek'),
    url(r'^penutupan-apotek/penutupan-apotek-done/$', views.penutupan_apotek_done, name='izin_dinkes__penutupan_apotek_done'),
	############### end Izin penutupan apotek ##########

	############### Izin optikal ##########
	url(r'^optikal/save-izin-optikal/$', views.save_izin_optikal, name='izin_dinkes__save_izin_optikal'),

	url(r'^optikal/upload-berkas-optikal/$', views.upload_berkas_optikal, name='izin_dinkes__upload_berkas_optikal'),
	url(r'^optikal/upload-berkas-optikal/save/$', views.optikal_upload_dokumen_cookie, name='izin_dinkes__upload_berkas_optikal_save'),
    url(r'^optikal/load-berkas/ajax/(?P<id_pengajuan>[0-9]+)$', views.ajax_load_berkas_optikal, name='izin_dinkes__ajax_load_berkas_optikal'),

    url(r'^optikal/load-konfirmasi-optikal/ajax/(?P<id_pengajuan>[0-9]+)$', views.load_konfirmasi_optikal, name='izin_dinkes__load_konfirmasi_optikal'),
    url(r'^optikal/optikal-done/$', views.optikal_done, name='izin_dinkes__optikal_done'),

	############### end Izin Lab ##########

	############### Izin Mendirikan Klinik ##########
	url(r'^klinik/save-izin-mendirikan-klinik/$', views.save_izin_mendirikan_klinik, name='izin_dinkes__save_izin_mendirikan_klinik'),
	url(r'^klinik/load-izin-mendirikan-klinik/(?P<id_pengajuan>[0-9]+)$', views.load_izin_mendirikan_klinik, name='izin_dinkes__load_izin_mendirikan_klinik'),

	url(r'^klinik/upload-berkas-mendirikan-klinik/$', views.upload_berkas_mendirikan_klinik, name='izin_dinkes__upload_berkas_mendirikan_klinik'),
	url(r'^klinik/upload-berkas-mendirikan-klinik/save/$', views.mendirikan_klinik_upload_dokumen_cookie, name='izin_dinkes__upload_berkas_mendirikan_klinik_save'),
    url(r'^klinik/load-berkas/ajax/(?P<id_pengajuan>[0-9]+)$', views.ajax_load_berkas_mendirikan_klinik, name='izin_dinkes__ajax_load_berkas_mendirikan_klinik'),

    url(r'^klinik/load-konfirmasi-mendirikan-klinik/ajax/(?P<id_pengajuan>[0-9]+)$', views.load_konfirmasi_mendirikan_klinik, name='izin_dinkes__load_konfirmasi_mendirikan_klinik'),
    url(r'^klinik/mendirikan-klinik-done/$', views.mendirikan_klinik_done, name='izin_dinkes__mendirikan_klinik_done'),
	############### END Izin Mendirikan Klinik ##########

	############### Izin Operasional Klinik ##########
	url(r'^klinik/save-izin-operasional-klinik/$', views.save_izin_operasional_klinik, name='izin_dinkes__save_izin_operasional_klinik'),
	url(r'^klinik/load-izin-operasional-klinik/(?P<id_pengajuan>[0-9]+)$', views.load_izin_operasional_klinik, name='izin_dinkes__load_izin_operasional_klinik'),

	url(r'^klinik/upload-berkas-operasional-klinik/$', views.upload_berkas_operasional_klinik, name='izin_dinkes__upload_berkas_operasional_klinik'),
	url(r'^klinik/upload-berkas-operasional-klinik/save/$', views.operasional_klinik_upload_dokumen_cookie, name='izin_dinkes__upload_berkas_operasional_klinik_save'),
    url(r'^klinik/load-berkas-operasional/ajax/(?P<id_pengajuan>[0-9]+)$', views.ajax_load_berkas_operasional_klinik, name='izin_dinkes__ajax_load_berkas_operasional_klinik'),

    url(r'^klinik/load-konfirmasi-operasional-klinik/ajax/(?P<id_pengajuan>[0-9]+)$', views.load_konfirmasi_operasional_klinik, name='izin_dinkes__load_konfirmasi_operasional_klinik'),
    url(r'^klinik/operasional-klinik-done/$', views.operasional_klinik_done, name='izin_dinkes__operasional_klinik_done'),
	############### END Izin Operasional Klinik ##########

	url(r'^proses/post-pengajuanizin-dinkes/(?P<obj_id>[0-9]+)$', views_dinkes.post_pengajuanizin_dinkes, name='izin_dinkes__post_pengajuanizin_dinkes'),
]