from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

admin.site.site_title = 'Sistem Informasi Manajemen Pelayanan Perijinan Terpadu Satu Pintu Kabupaten Kediri'

from simpdu.sites import usersite

admin.autodiscover()

#Admin
urlpatterns = [
	url(r'^admin/$', 'simpdu.views.admin_home', name='admin_home'),
    url(r'^user/$', 'simpdu.views.user_home', name='user_home'),
    url(r'^perusahaan/', include('perusahaan.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include(usersite.urls)),
    url(r'^',include('izin.urls')),
    url(r'^accounts/login/$', 'cas.views.login', name='login_cas'),
    url(r'^accounts/logout/$', 'cas.views.logout', name='logout_cas'),
    url(r'^accounts/login/failed/$', 'accounts.views.cas_failed', name='login_failed'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Login As
urlpatterns += patterns('loginas.views',
    url(r"^login/user/(?P<user_id>.+)/$", "user_login", name="loginas-user-login"),
)

# Front-end
urlpatterns += [
    url(r'^index-awal/$', 'simpdu.views.awal', name='awal'),
    url(r'^monitoring/$', 'simpdu.views.monitoring_berkas', name='monitoring_berkas'),
    url(r'^register/$', 'simpdu.views.register', name='register'),
    url(r'^syarat/$', "simpdu.views.syarat", name="syarat"),
    url(r'^syarat/izingangguan$', "simpdu.views.izingangguan", name="izingangguan"),
    url(r'^syarat/jasa_titipan$', "simpdu.views.jasa_titipan", name="jasa_titipan"),
    url(r'^syarat/lingkungan$', "simpdu.views.lingkungan", name="lingkungan"),
    url(r'^syarat/lokasi$', "simpdu.views.lokasi", name="lokasi"),
    url(r'^syarat/mendirikan_bangunan$', "simpdu.views.mendirikan_bangunan", name="mendirikan_bangunan"),
    url(r'^syarat/mendirikan_tower$', "simpdu.views.mendirikan_tower", name="mendirikan_tower"),
    url(r'^syarat/konstruksi_ruang_sungai$', "simpdu.views.konstruksi_ruang_sungai", name="konstruksi_ruang_sungai"),
    url(r'^syarat/mengubah_aliran_sungai$', "simpdu.views.mengubah_aliran_sungai", name="mengubah_aliran_sungai"),
    url(r'^syarat/tiang_pancang$', "simpdu.views.tiang_pancang", name="tiang_pancang"),
    url(r'^syarat/pemanfaatan_bantaran_sungai$', "simpdu.views.pemanfaatan_bantaran_sungai", name="pemanfaatan_bantaran_sungai"),
    url(r'^syarat/pematangan_lahan$', "simpdu.views.pematangan_lahan", name="pematangan_lahan"),
    url(r'^syarat/pembuangan_limbah$', "simpdu.views.pembuangan_limbah", name="pembuangan_limbah"),
    url(r'^syarat/pembuatan_jalan$', "simpdu.views.pembuatan_jalan", name="pembuatan_jalan"),
    url(r'^syarat/jalan_masuk_pekarangan$', "simpdu.views.jalan_masuk_pekarangan", name="jalan_masuk_pekarangan"),
    url(r'^syarat/tempat_parkir$', "simpdu.views.tempat_parkir", name="tempat_parkir"),
    url(r'^syarat/raung_milik_jalan$', "simpdu.views.ruang_milik_jalan", name="ruang_milik_jalan"),
    url(r'^syarat/penutupan_jalan$', "simpdu.views.penutupan_jalan", name="penutupan_jalan"),
    url(r'^syarat/reklame$', "simpdu.views.reklame", name="reklame"),
    url(r'^syarat/trayek$', "simpdu.views.trayek", name="trayek"),
    url(r'^syarat/usaha_angkutan$', "simpdu.views.usaha_angkutan", name="usaha_angkutan"),
    url(r'^syarat/usaha_industri$', "simpdu.views.usaha_industri", name="usaha_industri"),
    url(r'^syarat/usaha_jasa_konstruksi$', "simpdu.views.usaha_jasa_konstruksi", name="usaha_jasa_konstruksi"),
    url(r'^syarat/usaha_perdagangan$', "simpdu.views.usaha_perdagangan", name="usaha_perdagangan"),
    url(r'^syarat/daftar_gudang$', "simpdu.views.daftar_gudang", name="daftar_gudang"),
    url(r'^syarat/daftar_industri$', "simpdu.views.daftar_industri", name="daftar_industri"),
    url(r'^syarat/daftar_perusahaan$', "simpdu.views.daftar_perusahaan", name="daftar_perusahaan"),
    url(r'^syarat/daftar_usaha_kecil$', "simpdu.views.daftar_usaha_kecil", name="daftar_usaha_kecil"),
    url(r'^syarat/daftar_usaha_mikro$', "simpdu.views.daftar_usaha_mikro", name="daftar_usaha_mikro"),
    ]

