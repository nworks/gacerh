from django import forms
from models import UserP
from django.contrib.auth.models import User

class UsuarioForm(forms.ModelForm):
	first_name = forms.TextInput(attrs={'class': 'form-control'})
	last_name = forms.TextInput(attrs={'class': 'form-control'})
	email = forms.TextInput(attrs={'class': 'form-control'})
	class Meta:
		model = User
		fields = ["first_name","last_name","email"]


class LoginForm(forms.Form):
	username = forms.CharField(label=(u'Usuario'))
	password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))



class UserPr(forms.ModelForm):
		class Meta:
			model = UserP
			fields = ['cedula','empresa','puesto','telefono','celular','supervisor','email_super']



class UsuarioForm2(forms.ModelForm):
	class Meta:
		model = User
		fields = ["username","first_name","last_name","email","password"]



# forms.py
class PasswordResetRequestForm(forms.Form):
	email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)

class SetPasswordForm(forms.Form):
	"""
	A form that lets a user change set their password without entering the old
	password
	"""
	error_messages = {
		'password_mismatch': ("The two password fields didn't match."),
		}
	new_password1 = forms.CharField(label=("New password"),
									widget=forms.PasswordInput)
	new_password2 = forms.CharField(label=("New password confirmation"),
									widget=forms.PasswordInput)

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
