from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from izin.views import views, layanan_view, siup_view, reklame_view, iujk_views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'front-end/login.html'}, name='frontlogin'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': reverse_lazy('frontindex')}, name='frontlogout'),
    url(r'^$', views.frontindex, name='frontindex'),

    url(r'^layanan/siup$', layanan_view.layanan_siup, name='layanan_siup'),
    url(r'^layanan/ho-permohonan-baru$', layanan_view.layanan_ho_baru, name='layanan_ho_baru'),
    url(r'^layanan/ho-daftar-ulang$', layanan_view.layanan_ho_daftar_ulang, name='layanan_ho_daftar_ulang'),
    url(r'^layanan/sipa-sumur-bor$', layanan_view.layanan_sipa_sumur_bor, name='layanan_sipa_sumur_bor'),
    url(r'^layanan/sipa-sumur-pasak$', layanan_view.layanan_sipa_sumur_pasak, name='layanan_sipa_sumur_pasak'),
    url(r'^layanan/izin-pertambangan$', layanan_view.layanan_pertambangan, name='layanan_pertambangan'),
    url(r'^layanan/tdp-pt$', layanan_view.layanan_tdp_pt, name='layanan_tdp_pt'),
    url(r'^layanan/tdp-cv$', layanan_view.layanan_tdp_cv, name='layanan_tdp_cv'),
    url(r'^layanan/tdp-firma$', layanan_view.layanan_tdp_firma, name='layanan_tdp_firma'),
    url(r'^layanan/tdp-perorangan$', layanan_view.layanan_tdp_perorangan, name='layanan_tdp_perorangan'),
    url(r'^layanan/tdp-koperasi$', layanan_view.layanan_tdp_koperasi, name='layanan_tdp_koperasi'),
    url(r'^layanan/tdp-bul$', layanan_view.layanan_tdp_bul, name='layanan_tdp_bul'),
    url(r'^layanan/tdp-cabang$', layanan_view.layanan_tdp_baru_cabang, name='layanan_tdp_cabang'),
    url(r'^layanan/tdp-daftar-ulang$', layanan_view.layanan_tdp_daftar_ulang, name='layanan_tdp_daftar_ulang'),
    url(r'^layanan/reklame$', layanan_view.layanan_reklame, name='layanan_reklame'),
    url(r'^layanan/pemakaian-kekayaan$', layanan_view.layanan_kekayaan, name='layanan_kekayaan'),
    url(r'^layanan/penggilingan-padi-&-huller$', layanan_view.layanan_huller, name='layanan_huller'),
    url(r'^layanan/imb-umum$', layanan_view.layanan_imb_umum, name='layanan_imb_umum'),
    url(r'^layanan/imb-perumahan$', layanan_view.layanan_imb_perumahan, name='layanan_imb_perumahan'),
    url(r'^layanan/imb-reklame$', layanan_view.layanan_imb_reklame, name='layanan_imb_reklame'),
    url(r'^layanan/izin-prinsip-penanaman-modal$', layanan_view.layanan_izin_prinsip_penanaman_modal, name='layanan_izin_prinsip_penanaman_modal'),
    url(r'^layanan/izin-prinsip-perluasan-penanaman-modal$', layanan_view.layanan_izin_prinsip_perluasan_penanaman_modal, name='layanan_izin_prinsip_perluasan_penanaman_modal'),
    url(r'^layanan/izin-prinsip-perubahan-penanaman-modal$', layanan_view.layanan_izin_prinsip_perubahan_penanaman_modal, name='layanan_izin_prinsip_perubahan_penanaman_modal'),
    url(r'^layanan/izin-usaha-dan-izin-usaha-perluasan-penanaman-modal$', layanan_view.layanan_izin_usaha_dan_izin_usaha_perluasan_penanaman_modal, name='layanan_izin_usaha_dan_izin_usaha_perluasan_penanaman_modal'),
    url(r'^layanan/izin-usaha-perubahan-penanaman-modal$', layanan_view.layanan_izin_usaha_perubahan_penanaman_modal, name='layanan_izin_usaha_perubahan_penanaman_modal'),
    url(r'^layanan/izin-usaha-penggabungan-penanaman-modal$', layanan_view.layanan_izin_usaha_penggabunggan_penanaman_modal, name='layanan_izin_usaha_penggabunggan_penanaman_modal'),

    
    url(r'^404/', views.page_404, name='404'),
    url(r'^tentang/$', views.tentang, name='tentang'),
    url(r'^layanan/$', views.layanan, name='layanan'),
    url(r'^cari-pengajuan-izin/$', views.cari_pengajuan, name='cari_pengajuan'),
    url(r'^ajax-cek-pengajuan/$', views.ajax_cek_pengajuan, name='ajax_cek_pengajuan'),
    
    url(r'^layanan/siup/formulir$', views.formulir_siup, name='formulir_siup'),
    url(r'^layanan/ho-pemohonan-baru/formulir$', views.formulir_ho_pemohonan_baru, name='formulir_ho_pemohonan_baru'),
    url(r'^layanan/ho-daftar-ulang/formulir$', views.formulir_ho_daftar_ulang, name='formulir_ho_daftar_ulang'),
    url(r'^layanan/penggilingan-padi-&-huller/formulir$', views.formulir_huller, name='formulir_huller'),
    url(r'^layanan/reklame/formulir$', views.formulir_reklame, name='formulir_reklame'),
    url(r'^layanan/pemakaian-kekayaan/formulir$', views.formulir_kekayaan, name='formulir_kekayaan'),
    url(r'^layanan/tdp-pt/formulir$', views.formulir_tdp_pt, name='formulir_tdp_pt'),
    url(r'^layanan/imb-umum/formulir$', views.formulir_imb_umum, name='formulir_imb_umum'),
    url(r'^layanan/imb-perumahan/formulir$', views.formulir_imb_perumahan, name='formulir_imb_perumahan'),
    url(r'^layanan/imb-reklame/formulir$', views.formulir_imb_reklame, name='formulir_imb_reklame'),
    url(r'^layanan/tdp-cv/formulir$', views.formulir_tdp_cv, name='formulir_tdp_cv'),
    url(r'^layanan/tdp-firma/formulir$', views.formulir_tdp_firma, name='formulir_tdp_firma'),
    url(r'^layanan/tdp-perorangan/formulir$', views.formulir_tdp_perorangan, name='formulir_tdp_perorangan'),
    url(r'^layanan/tdp-koperasi/formulir$', views.formulir_tdp_koperasi, name='formulir_tdp_koperasi'),
    url(r'^layanan/tdp-bul/formulir$', views.formulir_tdp_bul, name='formulir_tdp_bul'),

    #cetak SIUP
    url(r'^layanan/siup/formulir/cetak/(?P<id_pengajuan_>[0-9A-Za-z_\-]+)$', views.cetak_permohonan, name='cetak_permohonan'),
    url(r'^layanan/siup/formulir/cetak-bukti-pendaftaran/(?P<id_pengajuan_>[0-9A-Za-z_\-]+)$', views.cetak_bukti_pendaftaran, name='cetak_bukti_pendaftaran'),

    #cetak HO Baru
    url(r'^layanan/ho-pemohonan-baru/formulir/cetak$', views.cetak_ho_perpanjang, name='cetak_ho_perpanjang'),
    url(r'^layanan/ho-pemohonan-baru/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_ho_baru, name='cetak_bukti_pendaftaran_ho_baru'),
    
    #cetak HO Perpanjang
    url(r'^layanan/ho-daftar-ulang/formulir/cetak$', views.cetak_ho_baru, name='cetak_ho_baru'),
    url(r'^layanan/ho-daftar-ulang/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_ho_perpanjang, name='cetak_bukti_pendaftaran_ho_perpanjang'),
    
    #cetak Penggilingan padi
    url(r'^layanan/penggilingan-padi-&-huller/formulir/cetak$', views.cetak_huller, name='cetak_huller'),
    url(r'^layanan/penggilingan-padi-&-huller/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_huller, name='cetak_bukti_pendaftaran_huller'),
    
    #cetak reklame
    url(r'^layanan/reklame/formulir/cetak$', views.cetak_reklame, name='cetak_reklame'),
    url(r'^layanan/reklame/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_reklame, name='cetak_bukti_pendaftaran_reklame'),
    
    #cetak Pemakaian Kekayaan
    url(r'^layanan/pemakaian-kekayaan/formulir/cetak$', views.cetak_kekayaan, name='cetak_kekayaan'),
    url(r'^layanan/pemakaian-kekayaan/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_kekayaan, name='cetak_bukti_pendaftaran_kekayaan'),

    #cetak IMB Umum
    url(r'^layanan/imb-umum/formulir/cetak$', views.cetak_imb_umum, name='cetak_imb_umum'),
    url(r'^layanan/imb-umum/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_imb_umum, name='cetak_bukti_pendaftaran_imb_umum'),

    #cetak IMB Perumahan
    url(r'^layanan/imb-perumahan/formulir/cetak$', views.cetak_imb_perumahan, name='cetak_imb_perumahan'),
    url(r'^layanan/imb-perumahan/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_imb_perumahan, name='cetak_bukti_pendaftaran_imb_perumahan'),

    #cetak IMB Reklame
    url(r'^layanan/imb-reklame/formulir/cetak$', views.cetak_imb_reklame, name='cetak_imb_reklame'),
    url(r'^layanan/imb-reklame/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_imb_reklame, name='cetak_bukti_pendaftaran_imb_reklame'),
    
    #cetak TDP PT
    url(r'^layanan/tdp-pt/formulir/cetak$', views.cetak_tdp_pt, name='cetak_tdp_pt'),
    url(r'^layanan/tdp-pt/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_tdp_pt, name='cetak_bukti_pendaftaran_tdp_pt'),
    
    #cetak TDP CV
    url(r'^layanan/tdp-cv/formulir/cetak$', views.cetak_tdp_cv, name='cetak_tdp_cv'),
    url(r'^layanan/tdp-cv/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_tdp_cv, name='cetak_bukti_pendaftaran_tdp_cv'),
    
    #cetak TDP FIRMA
    url(r'^layanan/tdp-firma/formulir/cetak$', views.cetak_tdp_firma, name='cetak_tdp_firma'),
    url(r'^layanan/tdp-firma/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_tdp_firma, name='cetak_bukti_pendaftaran_tdp_firma'),
    
    #cetak TDP PO
    url(r'^layanan/tdp-perorangan/formulir/cetak$', views.cetak_tdp_po, name='cetak_tdp_po'),
    url(r'^layanan/tdp-perorangan/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_tdp_po, name='cetak_bukti_pendaftaran_tdp_po'),
    
    #cetak TDP KOPERASI
    url(r'^layanan/tdp-koperasi/formulir/cetak$', views.cetak_tdp_koperasi, name='cetak_tdp_koperasi'),
    url(r'^layanan/tdp-koperasi/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_tdp_koperasi, name='cetak_bukti_pendaftaran_tdp_koperasi'),
    
    #cetak TDP Bul
    url(r'^layanan/tdp-bul/formulir/cetak$', views.cetak_tdp_bul, name='cetak_tdp_bul'),
    url(r'^layanan/tdp-bul/formulir/cetak-bukti-pendaftaran$', views.cetak_bukti_pendaftaran_tdp_bul, name='cetak_bukti_pendaftaran_tdp_bul'),


    # url for ajax siup
    url(r'^layanan/siup/pemohon/save/$', siup_view.siup_identitas_pemohon_save_cookie, name='siup_pemohon_save'),
    url(r'^layanan/siup/identitasperusahaan/save/$', siup_view.siup_identitas_perusahan_save_cookie, name='siup_identitas_perusahan_save'),
    url(r'^layanan/siup/detilsiup/save/$', siup_view.siup_detilsiup_save_cookie, name='siup_detilsiup_save'),
    url(r'^layanan/siup/legalitasperusahaan/save/$', siup_view.siup_legalitas_perusahaan_save_cookie, name='siup_legalitas_perusahaan_save'),
    url(r'^layanan/siup/upload/save/$', siup_view.siup_upload_dokumen_cookie, name='siup_upload_dokumen'),
    # url upload siup
    url(r'^layanan/siup/upload-berkas-foto-pemohon/save/$', siup_view.siup_upload_berkas_foto_pemohon, name='siup_upload_berkas_foto_pemohon'),
    url(r'^layanan/siup/upload-berkas-ktp-pemohon/save/$', siup_view.siup_upload_berkas_ktp_pemohon, name='siup_upload_berkas_ktp_pemohon'),
    url(r'^layanan/siup/upload-berkas-npwp-pribadi/save/$', siup_view.siup_upload_berkas_npwp_pribadi, name='siup_upload_berkas_npwp_pribadi'),
    url(r'^layanan/siup/upload-berkas-npwp-perusahaan/save/$', siup_view.siup_upload_berkas_npwp_perusahaan, name='siup_upload_berkas_npwp_perusahaan'),
    url(r'^layanan/siup/upload-berkas-akta-pendirian/save/$', siup_view.siup_upload_berkas_akta_pendirian, name='siup_upload_berkas_akta_pendirian'),
    url(r'^layanan/siup/upload-berkas-akta-perubahan/save/$', siup_view.siup_upload_berkas_akta_perubahan, name='siup_upload_berkas_akta_perubahan'),
    url(r'^layanan/siup/upload-berkas-pendukung/save/$', siup_view.siup_upload_berkas_pendukung, name='siup_upload_berkas_pendukung'),
    # end url upload siup
    url(r'^layanan/siup/save/$', siup_view.siup_done , name='siup_done'),
    url(r'^load-pemohon/(?P<ktp_>[0-9A-Za-z_\-]+)$', siup_view.load_pemohon , name='load_pemohon'),
    url(r'^load-perusahaan/(?P<npwp_>[0-9A-Za-z_\-.]+)$', siup_view.load_perusahaan , name='load_perusahaan'),
    # End
    # 
    # ++++++++++++++++++++++++ for ajax reklame ++++++++++++++++++++++
    url(r'^layanan/reklame/detilreklame/save/$', reklame_view.reklame_detilreklame_save_cookie, name='reklame_detilreklame_save'),
    url(r'^layanan/reklame/upload-berkas/save/$', reklame_view.reklame_upload_berkas_pendukung, name='reklame_upload_berkas_pendukung'),
    url(r'^layanan/reklame/upload/save/$', reklame_view.reklame_upload_dokumen_cookie, name='reklame_upload_dokumen'),
    # ++++++++++++++++++++++++ end for ajax reklame ++++++++++++++++++++++

    # AJAX SAVE IUJK
    url(r'^layanan/iujk/paketpekerjaan/save/$', iujk_views.iujk_paketpekerjaan_save, name='iujk_paketpekerjaan_save'),
    url(r'^layanan/iujk/paketpekerjaan/edit/(?P<id_paket_>[0-9]+)$', iujk_views.iujk_paketpekerjaan_edit, name='iujk_paketpekerjaan_edit'),
    url(r'^layanan/iujk/detiliujk/save/$', iujk_views.iujk_detiliujk_save, name='iujk_detiliujk_save'),
    url(r'^layanan/iujk/legalitasperusahaan/save/$', iujk_views.iujk_legalitas_perusahaan_save, name='iujk_legalitas_perusahaan_save'),
    url(r'^layanan/iujk/penanggungjawab/save/$', iujk_views.penanggung_jawab_save_bu, name='penanggung_jawab_save_bu'),
    url(r'^layanan/iujk/penanggungjawab/delete/$', iujk_views.penanggung_jawab_delete_bu, name='penanggung_jawab_delete_bu'),
    url(r'^layanan/iujk/penanggungjawabteknik/save/$', iujk_views.penanggung_jawab_teknik_save_bu, name='penanggung_jawab_teknik_save_bu'),
    url(r'^layanan/iujk/penanggungjawabnonteknik/save/$', iujk_views.penanggung_jawab_non_teknik_save_bu, name='penanggung_jawab_non_teknik_save_bu'),
    url(r'^layanan/iujk/penanggungjawab/next/$', iujk_views.penanggung_jawab_next, name='penanggung_jawab_next'),
    url(r'^layanan/iujk/uploaddokumen/sertifikat/$', iujk_views.upload_sertifikat_badan_usaha, name='upload_sertifikat_badan_usaha'),

    # END 
    ]
