from django.shortcuts import get_object_or_404, render
from Website.python import tools
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import User, Group
from challenge.models import Submission
from home.models import Picture
from .forms import CreateUserForm, LoginForm, CreateGroupForm

class UserView(generic.DetailView):
	model = User
	template_name = 'user/user.html'

def user(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	current_user = tools.validate_current_user(request.session, user.id)
	submissions = []
	for group in user.groups.all():
		for submission in Submission.objects.filter(group=group):
			if submission:
				submissions.append(submission)

	return render(request, 'user/user.html', {
		'user': user,
		'current_user': current_user,
		'submissions': submissions,
		})

def login(request):
	return render(request, 'user/login.html', {})

def logout(request):
	try:
		del request.session['user_id']
	except KeyError:
		pass

	return HttpResponseRedirect('/')

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
			pwd = form.cleaned_data['pwd']
			pwd_check = form.cleaned_data['pwd']

			if not pwd == pwd_check:
				raise ValidationError(_("Passwords don't match"), code='invalid')

			if not tools.verify_email(email):
				return HttpResponse("Invalid email")

			individual_group = Group(name=email.split("@")[0])
			individual_group.save()

			# If the user uploaded a profile picture
			if user_picture:
				user = User(name=name, email=email, grad_year=grad_year, password=pwd, user_picture=user_picture)
			else:
				user = User(name=name, email=email, grad_year=grad_year, password=pwd)

			user.save()
			user.groups.add(individual_group)
			request.session['user_id'] = user.id

			return HttpResponseRedirect('/user/' + str(user.id) + '/')
			
		else:
			return HttpResponse("Form is not valid")

	return render(request, 'user/create_user.html', {})

def create_user(request):
	return render(request, 'user/create_user.html', {})

def user_index(request):
	all_users = User.objects.order_by("name")
	return render(request, 'user/user_index.html', {
			'all_users': all_users,
		})

def change_user_picture(request, user_id):
	return render(request, 'user/change_user_picture.html', {
		'user_id': user_id,
		})

def process_change_user_picture(request, user_id):
	if (tools.validate_current_user(request, user_id)):
		if request.method == 'POST':
			form = ChangePictureForm(request.POST, request.FILES)
			if form.is_valid():
				user = get_object_or_404(User, pk=user_id)
				user_picture = form.cleaned_data['user_picture']
				user.user_picture = user_picture
				user.save()
				return HttpResponseRedirect('/user/' + str(user.id) + '/')
			else:
				return HttpResponse("Form is not valid")
		else:
			return HttpResponseRedirect('/user/' + str(user_id) + '/')
	else:
		return HttpResponse("Invalid credentials id=" + str(user_id) + ' when id should equal: ' + str(request.session['user_id']))

def group(request, group_id):
	group = get_object_or_404(Group, pk=group_id)
	group_members = User.objects.filter(groups=group)
	user = User.objects.get(pk=request.session['user_id'])
	user_in_group = (user in group_members)
	return render(request, 'user/group.html', {
			'group': group,
			'group_members': group_members,
			'user_in_group': user_in_group,
		})

def group_index(request):
	groups = Group.objects.all
	return render(request, 'user/group_index.html', {
			'groups': groups,
		})

def create_group(request):
	return render(request, 'user/create_group.html', {})

def process_new_group(request):
	if request.method == 'POST':
		form = CreateGroupForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			user = User.objects.get(pk=request.session['user_id'])
			new_group = Group(name=name)
			new_group.save()
			user.groups.add(new_group)
			user.save()

			return HttpResponseRedirect('/user/group' + str(new_group.id) + '/')
		else:
			return HttpResponse("Form is invalid")
	else:
		return HttpResponseRedirect('/user/create_group/')

def join_group(request, group_id):
	user = User.objects.get(pk=request.session['user_id'])
	group = Group.objects.get(pk=group_id)
	user.groups.add(group)
	user.save()

	return HttpResponseRedirect('/user/group' + str(group_id) + '/')

def leave_group(request, group_id):
	user = User.objects.get(pk=request.session['user_id'])
	group = Group.objects.get(pk=group_id)
	user.groups.remove(group)
	user.save()

	return HttpResponseRedirect('/user/groups/')

def test(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	pic = user.picture_set.all()[0]
	return render(request, 'user/test.html', 
		{
			'user': user,
			'picture': pic,
		})
