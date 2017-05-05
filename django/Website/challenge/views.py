from django.shortcuts import render, get_object_or_404
from Website.python import tools
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .models import Challenge, Submission, HelpComment
from home.models import User
from .forms import CommentForm

import datetime

def challenges_home(request):
	return render(request, 'challenge/index.html', {})

def challenge_page(request, challenge_id):
	challenge = get_object_or_404(Challenge, pk=challenge_id)
	latest_comment_list = HelpComment.objects.filter(comment_replied_to=None).filter(challenge=challenge).order_by('date')

	return render(request, 'challenge/challenge.html', 
		{
			'challenge': challenge,
			'latest_comment_list': latest_comment_list,
			'media_path': settings.MEDIA_ROOT,
		})

def index_help_comment(request, comment_id):
	comment = get_object_or_404(HelpComment, pk=comment_id)
	sub_comments = HelpComment.objects.filter(comment_replied_to=comment).order_by('date')
	return render(request, 'challenge/comment_index.html', {
			'comment': comment,
			'sub_comments': sub_comments,
		})

def help_comment(request, challenge_id, comment_id):
	challenge = get_object_or_404(Challenge, pk=challenge_id)

	try:
		comment_replied_to = HelpComment.objects.get(id=comment_id)
	except HelpComment.DoesNotExist:
		comment_replied_to = None

	return render(request, 'challenge/help_comment.html', 
		{
			'challenge': challenge,
			'comment_replied_to': comment_replied_to,
		})

def process_help_comment(request):
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment_text = form.cleaned_data['comment_text']
			challenge = Challenge.objects.get(id=form.cleaned_data['challenge_id'])
			user = User.objects.get(id=request.session['user_id'])
			date = tools.datetimenow()

			# If the comment being processed is a reply to another comment
			if (form.cleaned_data['comment_id'] == 0):
				help_comment = HelpComment(challenge=challenge, user=user, comment_text=comment_text, date=date)
			else:
				comment = HelpComment.objects.get(pk=form.cleaned_data['comment_id'])
				help_comment = HelpComment(challenge=challenge, user=user, comment_replied_to=comment, comment_text=comment_text, date=date)
				comment.num_replies += 1
				comment.save()
			help_comment.save()

			return HttpResponseRedirect('/challenge/' + str(challenge.id) + '/')
		else:
			return HttpResponse("Form is not valid")

	else:
		pass
		# do something here

# def test(request, challenge_id):
# 	challenge = get_object_or_404(Challenge, pk=challenge_id)
# 	return render (request, 'challenge/test_download.html',
# 		{
# 			'challenge': challenge,
# 			'media_path': settings.MEDIA_ROOT,
# 		})
