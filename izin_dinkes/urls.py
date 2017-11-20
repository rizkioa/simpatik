from django.conf import settings
from django.conf.urls import patterns, url, include

import views

urlpatterns = [
	url(r'^save-izin-apotek/$', views.save_izin_apotek, name='izin_dinkes__save_izin_apotek'),
]