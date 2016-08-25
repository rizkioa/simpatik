from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.contrib import messages

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon
from izin.models import PengajuanIzin, JenisPermohonanIzin
from izin.izin_forms import PengajuanBaruForm, PemohonForm

def add_wizard_siup(request):
	extra_context = {}
	extra_context.update({'title': 'Pengajuan Baru'})

	if request.method == 'POST':
		form = PengajuanBaruForm(request.POST)
		if request.POST.get('nama_izin'):
			id_nama_izin_ = request.POST.get('nama_izin') # Get name 'nama_izin' in request.POST
			id_kelompok_ = int(id_nama_izin_) # Convert unicode to int
			url_ = reverse('admin:izin_proses_siup')
			response = HttpResponseRedirect(url_) # Redirect to url
			response.set_cookie(key='id_kelompok_izin', value=id_kelompok_) # to set cookie in browser
			return response
		elif request.POST.get('nama_izin') and request.POST.get('kelompok_jenis_izin'):
			pass
		else:
			messages.warning(request, 'Anda belum memasukkan pilihan. Silahkan ulangi kembali.')
	else:
		form = PengajuanBaruForm()

	extra_context.update({'form': form })

	template = loader.get_template("admin/izin/izin/form_siup.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))


def formulir_siup(request):
	extra_context={}
	extra_context.update({'title': 'SIUP Baru'})
	negara = Negara.objects.all()
	extra_context.update({'negara': negara})
	provinsi = Provinsi.objects.all()
	extra_context.update({'provinsi': provinsi})
	kabupaten = Kabupaten.objects.all()
	extra_context.update({'kabupaten': kabupaten})
	kecamatan = Kecamatan.objects.all()
	extra_context.update({'kecamatan': kecamatan})
	desa = Desa.objects.all()
	extra_context.update({'desa': desa})
	jenis_pemohon = JenisPemohon.objects.all()
	extra_context.update({'jenis_pemohon': jenis_pemohon})
	jenispermohonanizin_list = JenisPermohonanIzin.objects.filter(jenis_izin__id=1) # Untuk SIUP

	print request.COOKIES
	extra_context.update({'jenispermohonanizin_list': jenispermohonanizin_list})

	form = PemohonForm()
	extra_context.update({'form': form})
	template = loader.get_template("admin/izin/izin/form_wizard_siup.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))
