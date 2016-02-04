from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from collections import OrderedDict
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm

class AccountChangeForm(UserChangeForm):

	class Meta:
		fields = '__all__'

	def clean_email(self):
		return self.cleaned_data['email'] or None

class CustomSetPasswordForm(forms.Form):
	"""
	A form that lets a user change set their password without entering the old
	password
	"""
	error_messages = {
		'password_mismatch': _("The two password fields didn't match."),
	}
	new_password1 = forms.CharField(label=_("New password"),
									widget=forms.PasswordInput)
	new_password2 = forms.CharField(label=_("New password confirmation"),
									widget=forms.PasswordInput)

	def __init__(self, user, *args, **kwargs):
		self.user = user
		super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
		if not self.user.has_usable_password():
			del self.fields['old_password']

	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 and password2:
			if password1 != password2:
				raise forms.ValidationError(
					self.error_messages['password_mismatch'],
					code='password_mismatch',
				)
		return password2

	def save(self, commit=True):
		self.user.set_password(self.cleaned_data['new_password1'])
		if commit:
			self.user.save()
		return self.user
		
class CustomPasswordChangeForm(CustomSetPasswordForm):
	"""
	A form that lets a user change their password by entering their old
	password.
	"""
	error_messages = dict(CustomSetPasswordForm.error_messages, **{
		'password_incorrect': _("Your old password was entered incorrectly. "
								"Please enter it again."),
	})
	old_password = forms.CharField(label="Old Password",
								   widget=forms.PasswordInput)


	def clean_old_password(self):
		"""
		Validates that the old_password field is correct.
		"""
		old_password = self.cleaned_data["old_password"]
		if self.user.has_usable_password():
			if not self.user.check_password(old_password):
				raise forms.ValidationError(
					self.error_messages['password_incorrect'],
					code='password_incorrect',
				)
		return old_password

CustomPasswordChangeForm.base_fields = OrderedDict(
	(k, CustomPasswordChangeForm.base_fields[k])
	for k in ['old_password', 'new_password1', 'new_password2']
)