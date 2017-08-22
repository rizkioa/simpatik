from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from tastypie.api import Api
from mobile.api import PengajuanIzinResource, AccountsResource, AuthResource
from izin.api import *
from perusahaan.api import PerusahaanResource, LegalitasResource, DataPimpinanResource, PemegangSahamResource
from master.api import BerkasResource, DesaResource

admin.site.site_title = 'Sistem Informasi Manajemen Pelayanan Perijinan Terpadu Satu Pintu Kabupaten Kediri'

from simpdu.sites import usersite
from .views import index

# from rest_framework_jwt.views import refresh_jwt_token
# from rest_framework_jwt.views import verify_jwt_token
# from mobile.cors import CORSObtainJSONWebToken
from mobile.views import request_user


admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(AuthResource())
v1_api.register(AccountsResource())
v1_api.register(PemohonResource())
v1_api.register(PerusahaanResource())
v1_api.register(KendaraanResource())
v1_api.register(BerkasResource())
v1_api.register(SKIzinResource())
v1_api.register(LegalitasResource())
v1_api.register(IzinLainResource())
v1_api.register(DataPimpinanResource())
v1_api.register(PemegangSahamResource())
v1_api.register(InformasiKekayaanDaerahResource())
v1_api.register(DesaResource())
v1_api.register(DetilHOResource())
v1_api.register(PengajuanIzinResource())
v1_api.register(DetilTDPResource())
v1_api.register(DetilIUAResource())
v1_api.register(DetilReklameResource())
v1_api.register(DetilReklameIzinResource())
v1_api.register(DetilIMBPapanReklameResource())
v1_api.register(DetilIMBResource())
v1_api.register(DetilHullerResource())
v1_api.register(InformasiTanahResource()) # Izin Lokasi
v1_api.register(SertifikatTanahResource()) # Izin Lokasi
v1_api.register(PenggunaanTanahIPPTUsahaResource()) # IPPT
v1_api.register(PerumahanYangDimilikiIPPTUsahaResource()) # IPPT
v1_api.register(MesinPerusahaanResource()) # Huller
v1_api.register(DetilIzinParkirIsidentilResource()) # Izin Parkir Dishub
v1_api.register(DataAnggotaParkirResource()) # Izin Parkir Dishub
v1_api.register(BerkasTerkalitIzin())
v1_api.register(DetilIUJKResource())
v1_api.register(PaketPekerjaanResource())

v2_api = Api(api_name='v2')
v2_api.register(PengajuanIzinAllResource())

# obtain_jwt_token = CORSObtainJSONWebToken.as_view()

#Admin
urlpatterns = [
    # url(r'^admin/$', 'simpdu.views.admin_home', name='admin_home'),
    # url(r'^api-token-auth/', obtain_jwt_token),
    # url(r'^api-token-login/', request_user),
    # url(r'^api-token-auth/', ObtainJSONWebToken.as_views()),
    # url(r'^api-token-refresh/', refresh_jwt_token),
    # url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/', include(v2_api.urls)),
	url(r'^admin/$', index, name='admin_home'),
    url(r'^user/$', 'simpdu.views.user_home', name='user_home'),
    # url(r'^s/', include('perusahaan.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include(usersite.urls)),
    url(r'^', include('izin.urls')),

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
    ]