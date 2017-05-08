from django.shortcuts import render
from django.http import HttpResponseRedirect
from challenge.models import Challenge

def home(request):
	return render(request, 'home/index.html', {})

def about(request):
	return HttpResponseRedirect('/static/text/file_format_guidelines.txt')
