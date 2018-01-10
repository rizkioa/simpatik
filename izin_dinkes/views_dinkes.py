from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from izin.models import PengajuanIzin
from izin.utils import get_model_detil
from master.models import Settings
import json
import requests

@login_required
def post_pengajuanizin_dinkes(request, obj_id):
	respon_data = {'success': False, 'pesan': 'Terjadi kesalahan server'}
	try:
		pengajuan_obj = PengajuanIzin.objects.get(id=obj_id)
		kelompok_izin = pengajuan_obj.kelompok_jenis_izin.kode
		try:
			detilizin_obj = get_model_detil(kelompok_izin).objects.get(id=pengajuan_obj.id)
			url_api_obj = Settings.objects.filter(parameter='API URL PENGAJUAN DINKES').last()
			url_api_simpatik_dinkes = str(url_api_obj.url)+'pengajuan-izin-list/'
			# print url_api_simpatik_dinkes
			if kelompok_izin == 'IAP':
				perusahaan = detilizin_obj.nama_apotek
			elif kelompok_izin == 'ILB':
				perusahaan = detilizin_obj.nama_laboratorium
			elif kelompok_izin == 'IOP':
				perusahaan = detilizin_obj.nama_optikal
			elif kelompok_izin == 'IPA':
				perusahaan = detilizin_obj.nama_apotek
			elif kelompok_izin == 'ITO':
				perusahaan = detilizin_obj.nama_toko_obat

			data = {'id_pengajuan_simpatik':pengajuan_obj.id,
					'no_pengajuan': pengajuan_obj.no_pengajuan,
					'perusahaan':perusahaan,
					'pemohon':pengajuan_obj.pemohon.nama_lengkap,
					'jenis_pengajuan':pengajuan_obj.kelompok_jenis_izin.kode,
					'tgl_pengajuan':pengajuan_obj.created_at.strftime('%Y-%m-%d')
				}

			headers = {'content-type': 'application/json'}

			r = requests.post(url_api_simpatik_dinkes, data=json.dumps(data), headers=headers)
			print r.json()
			respon = r.json()
			if respon.get('success'):
				if respon.get('success') == True:
					s = pengajuan_obj.survey_pengajuan.all()
					s.status = 8
					
					pengajuan_obj.status = 8
					pengajuan_obj.save()

					respon_data = {'success': True, 'pesan': 'Data berhasil dikirim'}
				else:
					respon_data = {'success': False, 'pesan': respon.get('pesan')}
			else:
				respon_data = {'success': False, 'pesan': respon.get('pesan')}
		except ObjectDoesNotExist:
			respon_data = {'success': False, 'pesan': 'Kelompok jenis izin tidak ditemukan'}
	except PengajuanIzin.DoesNotExist:
		respon_data = {'success': False, 'pesan': 'Terjadi kesalahan server'}
	return HttpResponse(json.dumps(respon_data))