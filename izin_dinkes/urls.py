from django.conf import settings
from django.conf.urls import patterns, url, include

import views

urlpatterns = [
	url(r'^save-izin-apotek/$', views.save_izin_apotek, name='izin_dinkes__save_izin_apotek'),
	url(r'^save-izin-toko-obat/$', views.save_izin_toko_obat, name='izin_dinkes__save_izin_toko_obat'),
]