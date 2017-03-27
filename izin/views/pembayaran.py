from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin import site
from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs
from django.core.exceptions import ObjectDoesNotExist

from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from django.views import generic
import base64
import time
import json
import os

from izin.models import PengajuanIzin, DetilIMB,DetilPembayaran,SKIzin,Riwayat
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import DetilPembayaranForm

def detil_pembayaran_save(request):
	if request.POST:
		pengajuan_izin_id = request.POST.get('pengajuan_izin', None)
		pengajuan_izin = PengajuanIzin.objects.get(id=pengajuan_izin_id)
		try:
			pengajuan_ = DetilPembayaran.objects.get(pengajuan_izin__id=pengajuan_izin_id)
			sk_izin_ = SKIzin.objects.get(pengajuan_izin__id=pengajuan_izin_id)
			pembayaran = DetilPembayaranForm(request.POST, instance=pengajuan_)
		except ObjectDoesNotExist:
			pembayaran = DetilPembayaranForm(request.POST)

		if pembayaran.is_valid():
			if request.user.groups.filter(name='Kasir'):
				p = pembayaran.save(commit=False)
				p.save()
				sk_izin_.status = 4
				sk_izin_.save()
				pengajuan_izin.status = 2
				pengajuan_izin.save()
				riwayat_ = Riwayat(
					pengajuan_izin_id = pengajuan_izin.id,
					created_by_id = request.user.id,
					keterangan = "Kasir Verified"
				)
				riwayat_.save()

				data = {'success': True,
						'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
						'data': {}}
				response = HttpResponse(json.dumps(data))
			else:
				p = pembayaran.save(commit=False)
				p.save()
				pengajuan_izin.status = 4
				pengajuan_izin.save()
				riwayat_ = Riwayat(
					pengajuan_izin_id = pengajuan_izin.id,
					created_by_id = request.user.id,
					keterangan = "Operator Verified"
				)
				riwayat_.save()

				data = {'success': True,
						'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
						'data': {}}
				response = HttpResponse(json.dumps(data))
		else:
			data = pembayaran.errors.as_json()
			response = HttpResponse(data)

		return response