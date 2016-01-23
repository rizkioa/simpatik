from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

from simpdu.sites import usersite

admin.autodiscover()

#Admin
urlpatterns = [
	url(r'^admin/$', 'simpdu.views.admin_home', name='admin_home'),
    url(r'^user/$', 'simpdu.views.user_home', name='user_home'),


    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include(usersite.urls)),

    url(r'^accounts/login/$', 'cas.views.login', name='login_cas'),
    url(r'^accounts/logout/$', 'cas.views.logout', name='logout_cas'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Login As
urlpatterns += patterns('loginas.views',
    url(r"^login/user/(?P<user_id>.+)/$", "user_login", name="loginas-user-login"),
)

# Front-end
urlpatterns += [
    url(r'^$', 'simpdu.views.welcome', name='welcome'),
]

