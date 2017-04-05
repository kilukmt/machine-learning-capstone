from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import User, Group
from .forms import CreateUserForm

class UserView(generic.DetailView):
	model = User
	template_name = 'user/user.html'

def create_user(request):
	return render(request, 'user/create_user.html', {})

def process_new_user(request):
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			grad_year = form.cleaned_data['grad_year']

			# Validate email here!!!

			user = User(name=name, email=email, grad_year=grad_year)
			user.save()

			return HttpResponseRedirect('/user/' + str(user.id) + '/')
		else:
			return HttpResponse("Form is not valid")

	return render(request, 'user/create_user.html', {})
