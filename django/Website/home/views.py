from django.shortcuts import render
from Website.python import tools
from challenge.models import Challenge

def home(request):
	return render(request, 'home/index.html', {})
