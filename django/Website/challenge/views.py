from django.shortcuts import render, get_object_or_404
from Website.python import tools
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from .models import Challenge, Submission, HelpComment
from user.models import User, Group
from .forms import CommentForm, SubmissionForm

import datetime

def challenges_home(request):
	latest_challenge_list = Challenge.get_latest_challenges(5)
	popular_challenge_list = Challenge.get_popular_challenges(5)
	all_challenges = Challenge.objects.order_by('challenge_name')
	return render(request, 'challenge/index.html', {
			'latest_challenge_list': latest_challenge_list,
			'popular_challenge_list': popular_challenge_list,
			'all_challenges': all_challenges,
		})

def challenge_page(request, challenge_id):
	challenge = get_object_or_404(Challenge, pk=challenge_id)
	latest_comment_list = HelpComment.objects.filter(comment_replied_to=None).filter(challenge=challenge).order_by('date')
	submissions = Submission.objects.filter(challenge=challenge).order_by('-error_rate')[:100]

	return render(request, 'challenge/challenge.html', 
		{
			'challenge': challenge,
			'latest_comment_list': latest_comment_list,
			'submissions': submissions,
			'media_path': settings.MEDIA_ROOT,
		})

def submit(request, challenge_id):
	challenge = get_object_or_404(Challenge, pk=challenge_id)
	groups = tools.get_session_groups(request.session)

	if groups:
		return render(request, 'challenge/submit.html', {
				"challenge": challenge,
				"groups": groups,
			})
	else:
		return HttpResponseRedirect('/user/login/')

def process_submit(request):
	if request.method == 'POST':
		form = SubmissionForm(request.POST, request.FILES)
		if form.is_valid():
			challenge = Challenge.objects.get(id=form.cleaned_data['challenge_id'])
			group = Group.objects.get(name=form.cleaned_data['group'])
			user = User.objects.get(id=form.cleaned_data['user_id'])
			submission_file = form.cleaned_data['submission_file']

			if tools.submission_is_valid(submission_file):
				test_key = challenge.test_key
				error_rate = tools.evaluate_submission(submission_file, test_key)
			else:
				return HttpResponseRedirect('/challenge/' + challenge.id + '/submit')

			if form.cleaned_data['code_files'] == None:
				submission = Submission(challenge=challenge, group=group, user=user, error_rate=error_rate, latest_submission=tools.datetimenow())
			else:
				submission = Submission(challenge=challenge, group=group, user=user, error_rate=error_rate,\
										latest_submission=tools.datetimenow(), code_files=form.cleaned_data['code_files'])

			submission.save()
			return render(request, 'challenge/submission_results.html', {
					'challenge': challenge,
					'error_rate': error_rate,
				})
		else:
			return HttpResponse("Form is invalid")
	else:
		return HttpResponse("Invalid request")

def index_help_comment(request, comment_id):
	comment = get_object_or_404(HelpComment, pk=comment_id)
	sub_comments = HelpComment.objects.filter(comment_replied_to=comment).order_by('date')
	return render(request, 'challenge/comment_index.html', {
			'comment': comment,
			'sub_comments': sub_comments,
		})

def help_comment(request, challenge_id, comment_id=0):
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
