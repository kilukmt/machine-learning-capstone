from django import forms

class CreateUserForm(forms.Form):
	name = forms.CharField(label='name', max_length=100)
	email = forms.EmailField(label='email')
	grad_year = forms.IntegerField(label='grad_year')
	user_picture = forms.ImageField(label='user_picture')
