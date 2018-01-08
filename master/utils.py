from models import Settings

def get_param(parameter_):
	sett_ = None
	sett_list = Settings.objects.filter(parameter=parameter_)
	if sett_list.exists():
		sett_ = sett_list.last()
	return sett_