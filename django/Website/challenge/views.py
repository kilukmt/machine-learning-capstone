from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from .models import Challenge, Submission, HelpComment

def challenge_page(request, challenge_id):
	challenge = get_object_or_404(Challenge, pk=challenge_id)
	
	return render(request, 'challenge/index.html', 
		{
			'challenge': challenge,
			'media_path': settings.MEDIA_ROOT,
		})

# def test(request, challenge_id):
# 	challenge = get_object_or_404(Challenge, pk=challenge_id)
# 	return render (request, 'challenge/test_download.html',
# 		{
# 			'challenge': challenge,
# 			'media_path': settings.MEDIA_ROOT,
# 		})
