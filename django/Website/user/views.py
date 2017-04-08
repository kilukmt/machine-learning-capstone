from django.shortcuts import get_object_or_404, render
from Website.python import tools
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import User, Group
from home.models import Picture
from .forms import CreateUserForm

class UserView(generic.DetailView):
	model = User
	template_name = 'user/user.html'

def process_new_user(request):
	if request.method == 'POST':
		form = CreateUserForm(request.POST, request.FILES)
		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			grad_year = form.cleaned_data['grad_year']

			# Validate email here!!!

			user = User(name=name, email=email, grad_year=grad_year)
			user.save()
			tools.handle_uploaded_pic(request.FILES['user_picture'], user.id)	# No need to save again, function has id of object and saves within the function
			return HttpResponseRedirect('/user/' + str(user.id) + '/')
		else:
			return HttpResponse("Form is not valid")

	return render(request, 'user/create_user.html', {})

def create_user(request):
	return render(request, 'user/create_user.html', {})

def test(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	pic = user.picture_set.all()[0]
	return render(request, 'user/test.html', 
		{
			'user': user,
			'picture': pic,
		})
