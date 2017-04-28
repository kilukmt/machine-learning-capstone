from django.shortcuts import get_object_or_404, render
from Website.python import tools
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import User, Group
from home.models import Picture
from .forms import CreateUserForm, LoginForm

class UserView(generic.DetailView):
	model = User
	template_name = 'user/user.html'

def user(request, pk):
	user = get_object_or_404(User, pk=pk)
	current_user = tools.validate_current_user(request.session, user.id)

	return render(request, 'user/user.html', {
		'user': user,
		'current_user': current_user,
		})

def login(request):
	return render(request, 'user/login.html', {})

def process_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = User.objects.get(email=request.POST['email'])
			if user.password == request.POST['pwd']:
				request.session['user_id'] = user.id
				return HttpResponseRedirect('/user/' + str(user.id) + '/')
			else:
				return HttpResponseRedirect('/user/login/')
		else:
			return HttpResponse("Form is not valid")

def process_new_user(request):
	if request.method == 'POST':
		form = CreateUserForm(request.POST, request.FILES)
		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			grad_year = form.cleaned_data['grad_year']
			user_picture = form.cleaned_data['user_picture']

			# Validate email here!!!

			user = User(name=name, email=email, grad_year=grad_year, user_picture=user_picture)
			user.save()

			return HttpResponseRedirect('/user/' + str(user.id) + '/')
			
		else:
			return HttpResponse("Form is not valid")

	return render(request, 'user/create_user.html', {})

def create_user(request):
	return render(request, 'user/create_user.html', {})

def change_user_picture(request, pk):
	return render(request, 'user/change_user_picture.html', {
		'pk': pk,
		})

def process_change_user_picture(request, pk):
	if (tools.validate_current_user(request, pk)):
		if request.method == 'POST':
			form = ChangePictureForm(request.POST, request.FILES)
			if form.is_valid():
				user = get_object_or_404(User, pk=pk)
				user_picture = form.cleaned_data['user_picture']
				user.user_picture = user_picture
				user.save()
				return HttpResponseRedirect('/user/' + str(user.id) + '/')
			else:
				return HttpResponse("Form is not valid")
		else:
			return HttpResponseRedirect('/user/' + str(pk) + '/')
	else:
		return HttpResponse("Invalid credentials id=" + str(pk) + ' when id should equal: ' + str(request.session['user_id']))

def test(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	pic = user.picture_set.all()[0]
	return render(request, 'user/test.html', 
		{
			'user': user,
			'picture': pic,
		})
