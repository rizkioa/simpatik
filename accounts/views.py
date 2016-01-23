from django.shortcuts import render

# Create your views here.
def login_as(request, target_user):
	if not request.user.is_superuser:
		return False
	return True