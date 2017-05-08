from django import forms

class CreateUserForm(forms.Form):
	name = forms.CharField(label='name', max_length=100)
	email = forms.EmailField(label='email')
	grad_year = forms.IntegerField(label='grad_year')
	user_picture = forms.ImageField(label='user_picture', required=False)
	pwd = forms.CharField(label='pwd', max_length=100)
	pwd_check = forms.CharField(label='pwd_check', max_length=100)

class LoginForm(forms.Form):
	email = forms.CharField(label='email', max_length=100)
	pwd = forms.CharField(label='pwd', max_length=100)

class ChangePictureForm(forms.Form):
	user_picture = forms.ImageField(label='user_picture')

class CreateGroupForm(forms.Form):
	group_name = forms.CharField(label='group_name', max_length=100)
	
