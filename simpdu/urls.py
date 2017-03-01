from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from tastypie.api import Api
from mobile.api import PengajuanIzinResource

admin.site.site_title = 'Sistem Informasi Manajemen Pelayanan Perijinan Terpadu Satu Pintu Kabupaten Kediri'

from simpdu.sites import usersite
from .views import index


admin.autodiscover()

v1_api = Api(api_name='pengajuanizin')
v1_api.register(PengajuanIzinResource())

#Admin
urlpatterns = [
    # url(r'^admin/$', 'simpdu.views.admin_home', name='admin_home'),
    url(r'^api/', include(v1_api.urls)),
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