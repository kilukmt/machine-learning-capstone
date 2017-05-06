import os

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.core.files.storage import FileSystemStorage as FSS
from Website.python import tools

class Challenge(models.Model):
	challenge_name = models.CharField(max_length=100)
	challenge_description = models.TextField()
	challenge_files = models.FileField(upload_to="challenges\\", max_length=300, default='\\challenges\\default.zip')
	date_created = models.DateTimeField('date_created')
	challenge_image = models.ImageField(upload_to="challenges\\challenge_avis\\", max_length=300, default='\\challenges\\challenge_avis\\default.jpg')
	test_key = models.TextField(blank=True, null=True)
	submission_count = models.IntegerField(default=0)

	# If a teacher wants to use the website to create a challenge,
	# give them the power to require students upload their code for the challenge too
	code_required = models.BooleanField(default=False)

	def save(self):
		super(Challenge, self).save()
		zip_filepath = settings.MEDIA_ROOT + self.challenge_files.name
		(valid_challenge_files, test_key) = tools.validate_challenge_files(zip_filepath)
		if valid_challenge_files:
			self.test_key = test_key
			super(Challenge, self).save()
			pass
		else:
			os.remove(zip_filepath)
			self.delete()
			raise Exception("Challenge files invalid")

	# returns a list of the "num_challenges_requested" most recent Challenge objects
	def get_latest_challenges(num_challenges_requested):
		return Challenge.objects.order_by('date_created')[:num_challenges_requested]
	
	# returns a list of the "num_challenges_requested" most popular Challenge objects (by submission count)
	def get_popular_challenges(num_challenges_requested):
		return Challenge.objects.order_by('submission_count')[:num_challenges_requested]

	def __str__(self):
		return self.challenge_name

class Submission(models.Model):
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, default=1)
	group = models.ForeignKey('user.Group', on_delete=models.CASCADE, default=1)
	user = models.ForeignKey('user.User', null=True, on_delete=models.SET_NULL)
	error_rate = models.DecimalField(max_digits=3, decimal_places=3)
	latest_submission = models.DateTimeField('latest_submission')
	code_files = models.FileField(upload_to="groups\\", max_length=300, blank=True, null=True)


	def __str__(self):
		d = str(self.latest_submission).split()
		d = d[0] + "_" + d[1].split("+")[0]
		return  self.challenge.challenge_name + "_" + self.group.name + "_" + d

def submission_post_save(sender, instance, **kwargs):

	# Delete the submission files to free up space on server
	SubmissionProcessingBuffer.objects.get(pk=instance.id).delete()

	# Increment the submission count of the challenge submitted to 
	challenge_submitted_to = instance.challenge
	challenge_submitted_to.submission_count += 1
	challenge_submitted_to.save()
post_save.connect(submission_post_save, sender=Submission)

def submission_post_delete(sender, instance, **kwargs):
	# Decrement the submission count of the challenge that was submitted to
	challenge_submitted_to = instance.challenge
	challenge_submitted_to.submission_count -= 1
	challenge_submitted_to.save()
post_delete.connect(submission_post_delete, sender=Submission)

class SubmissionProcessingBuffer(models.Model):
	group = models.ForeignKey(Submission, on_delete=models.CASCADE)
	submission_files = models.FileField(upload_to="groups\\", max_length=300, default='\\groups\\default.txt')


class HelpComment(models.Model):
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, default=1)
	user = models.ForeignKey('user.User', on_delete=models.CASCADE, default=1)
	comment_replied_to = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
	comment_text = models.TextField()
	date = models.DateTimeField('date written')
	num_replies = models.IntegerField(default=0)
	up_votes = models.IntegerField(default=0)
	down_votes = models.IntegerField(default=0)
	pictures = models.ManyToManyField('home.Picture')

	def __str__(self):
		d = str(self.date).split()
		d = d[0] + "_" + d[1].split("+")[0]
		return self.user.name + "_" + d
