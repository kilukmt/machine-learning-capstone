from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import User, Group

# class CreateUserView(generic.DetailView):
# 	model = User
# 	template_name = 'user/create_user.html'

# class IndexView(generic.DetailView):
# 	model = User
# 	template_name = 'user/index.html'

def create_user(request):
	return render(request, 'user/create_user.html', {})
