from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.admin import site
from functools import wraps
from django.views.decorators.cache import cache_page
from django.utils.decorators import available_attrs
from django.core.exceptions import ObjectDoesNotExist

from izin.izin_forms import PengajuanReklameForm
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

from izin.models import PengajuanIzin, DetilIMB,DetilSkIMB
from accounts.models import IdentitasPribadi, NomorIdentitasPengguna
from izin.izin_forms import DetilSkIMBForm

def detil_sk_imb_save(request):
	if request.POST:
		pengajuan_izin_id = request.POST.get('pengajuan_izin', None)
		try:
			pengajuan_ = DetilSkIMB.objects.get(pengajuan_izin__id=pengajuan_izin_id)
			Sk_IMB = DetilSkIMBForm(request.POST, instance=pengajuan_)
		except ObjectDoesNotExist:
			Sk_IMB = DetilSkIMBForm(request.POST)

		if Sk_IMB.is_valid():
			p = Sk_IMB.save(commit=False)
			p.save()
			data = {'success': True,
					'pesan': 'Data berhasil disimpan. Proses Selanjutnya.',
					'data': ['']}
			data = json.dumps(data)
			response = HttpResponse(json.dumps(data))
		else:
			data = Sk_IMB.errors.as_json()
			response = HttpResponse(data)

	return response