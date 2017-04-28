from django import forms

class CreateUserForm(forms.Form):
	name = forms.CharField(label='name', max_length=100)
	email = forms.EmailField(label='email')
	grad_year = forms.IntegerField(label='grad_year')
	user_picture = forms.ImageField(label='user_picture')

class LoginForm(forms.Form):
	email = forms.CharField(label='email', max_length=100)
	pwd = forms.CharField(label='pwd', max_length=100)

class ChangePictureForm(forms.Form):
	user_picture = forms.ImageField(label='user_picture')
