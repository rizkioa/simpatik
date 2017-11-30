from izin import models as app_models

def get_model_detil(kode):
	objects_ = None
	if kode and kode is not None:
		if kode == "503.08":
			objects_ = getattr(app_models, 'DetilSIUP')
		elif kode == "IUJK":
			objects_ = getattr(app_models, 'DetilIUJK')
		elif kode == "503.03.01/" or kode == "503.03.02/":
			objects_ = getattr(app_models, 'DetilReklame')
		elif kode == "TDP-PT" or kode == "TDP-CV" or kode == "TDP-FIRMA" or kode == "TDP-PERORANGAN" or kode == "TDP-BUL" or kode == "TDP-KOPERASI":
			objects_ = getattr(app_models, 'DetilTDP')
		elif kode == "503.01.06/":
			objects_ = getattr(app_models, 'DetilIMBPapanReklame')
		elif kode == "503.01.05/" or kode == "503.01.04/" :
			objects_ = getattr(app_models, 'DetilIMB')
		elif kode == "503.06.01/":
			objects_ = getattr(app_models, 'InformasiKekayaanDaerah')
		elif kode == "503.02/":
			objects_ = getattr(app_models, 'DetilHO')
		elif kode == "503.07/" or kode == "IPPT-Rumah" or kode == "IPPT-Usaha":
			objects_ = getattr(app_models, 'InformasiTanah')
		elif kode == "HULLER":
			objects_ = getattr(app_models, 'DetilHuller')
		elif kode == "TDUP":
			objects_ = getattr(app_models, 'DetilTDUP')
	return objects_