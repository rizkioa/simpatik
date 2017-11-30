from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import drest, json 

def get_rekomendasi_pembangunan(request):
	api_url = request.GET.get('api_url')
	id_ = request.GET.get('id')
	try:
		try:
			try :
				api = drest.api.TastyPieAPI("http://simpatik.kedirikab.go.id:8889/"+str(api_url))
				id_survey = dict(survey_iujk=id_)
				response = api.rekomendasi.get(params=id_survey)
				if response.status in (200, 201, 202) :
						try :
							obj_data = response.data['objects']
							data = {'success': True, 'pesan': obj_data }
						except KeyError:
							data = {'success': False, 'pesan': 'Object Tidak Diketahui.' }
			except drest.exc.dRestAPIError :
				data = {'success': False, 'pesan': '[APIError] Koneksi Server Pembangunan error 1.' }
		except drest.exc.dRestRequestError :
			data = {'success': False, 'pesan': '[RequestError] Koneksi Server Pembangunan error 2.' }
	except Exception, e:
		data = {'success': False, 'pesan': '[Exception] Error: '+str(e)+'.' }


	data = json.dumps(data)
	response = HttpResponse(data)
	return response