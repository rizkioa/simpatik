from django.http import HttpResponse
from django.template import RequestContext, loader

from master.models import Negara, Provinsi, Kabupaten, Kecamatan, Desa, JenisPemohon


def add_wizard_siup(request):
	extra_context = {}
	extra_context.update({'title': 'Pengajuan Baru'})
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

	template = loader.get_template("admin/izin/izin/form_wizard_siup.html")
	ec = RequestContext(request, extra_context)
	return HttpResponse(template.render(ec))