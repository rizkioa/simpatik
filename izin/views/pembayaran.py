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
from izin.utils import send_email_html

def detil_pembayaran_save(request):
	if request.POST:
		pengajuan_izin_id = request.POST.get('pengajuan_izin', None)
		try:
			detilpembayaran_obj = DetilPembayaran.objects.filter(pengajuan_izin__id=pengajuan_izin_id).last()
			sk_izin_ = SKIzin.objects.get(pengajuan_izin__id=pengajuan_izin_id)
			pembayaran = DetilPembayaranForm(request.POST, instance=detilpembayaran_obj)
		except ObjectDoesNotExist:
			pembayaran = DetilPembayaranForm(request.POST)
		if pembayaran.is_valid():
			if request.user.groups.filter(name='Kasir'):
				p = pembayaran.save(commit=False)
				p.kode = request.POST.get('kode')
				p.peruntukan = request.POST.get('peruntukan')
				p.pengajuan_izin_id = pengajuan_izin_id
				p.save()
				# sk_izin_.status = 9
				# sk_izin_.save()
				# detilpembayaran_obj.pengajuan_izin.status = 2
				# detilpembayaran_obj.pengajuan_izin.save()
				riwayat_ = Riwayat(
					pengajuan_izin_id = p.pengajuan_izin.id,
					created_by_id = request.user.id,
					keterangan = "Kasir Verified"
				)
				riwayat_.save()
				if p.pengajuan_izin.pemohon:
					if p.pengajuan_izin.pemohon.email and p.pengajuan_izin.pemohon.email is not None:
						send_email_html(p.pengajuan_izin.pemohon.email, p.peruntukan, p, 'cetak/notifikasi_send_email.html')

					data = {'success': True,
							'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
							'data': {}}
					response = HttpResponse(json.dumps(data))
			elif request.user.groups.filter(name='Operator') or request.user.is_superuser:
					p = pembayaran.save(commit=False)
					p.save()
					p.pengajuan_izin.status = 4
					p.pengajuan_izin.save()
					riwayat_ = Riwayat(
						pengajuan_izin_id = p.pengajuan_izin.id,
						created_by_id = request.user.id,
						keterangan = "Operator Verified"
					)
					riwayat_.save()

					data = {'success': True,
							'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
							'data': {}}
					response = HttpResponse(json.dumps(data))
			else:
				p = pembayaran.save(commit=False)
				p.save()
				p.pengajuan_izin.status = 5
				p.pengajuan_izin.save()
				riwayat_ = Riwayat(
					pengajuan_izin_id = p.pengajuan_izin.id,
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
	else:
		data = {'success': False,
						'pesan': 'Terjadi Kesalahan Pengajuan Tidak Ditemukan',
						'data': {}}
		response = HttpResponse(json.dumps(data))
	return response