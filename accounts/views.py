from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

# Create your views here.
def login_as(request, target_user):
	if not request.user.is_superuser:
		return False
	return True

def cas_failed(request):
	messages.warning(request, "Login Gagal, User tidak terdaftar di Sistem Pelayanan Perijinan Terpadu Satu Pintu.")
	return HttpResponseRedirect(reverse('logout_cas') + "?" + request.META['QUERY_STRING'])