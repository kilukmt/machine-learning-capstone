import os

from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
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

		if self.challenge_files.name == None:
			return

		zip_filepath = settings.MEDIA_ROOT + self.challenge_files.name
		(valid_challenge_files, test_key) = tools.validate_challenge_files(zip_filepath)
		if valid_challenge_files:
			self.test_key = test_key
			super(Challenge, self).save()
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

def challenge_pre_delete(sender, instance, **kwargs):
	instance.challenge_files.delete()

	if not instance.challenge_image.name.split("\\")[-1] == "default.jpg":
		instance.challenge_image.delete()

pre_delete.connect(challenge_pre_delete, sender=Challenge)

class Submission(models.Model):
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, default=1)
	group = models.ForeignKey('user.Group', on_delete=models.CASCADE, default=1)
	user = models.ForeignKey('user.User', null=True, on_delete=models.SET_NULL)
	error_rate = models.DecimalField(max_digits=4, decimal_places=3)
	latest_submission = models.DateTimeField('latest_submission')
	code_files = models.FileField(upload_to="groups\\", max_length=300, blank=True, null=True)


	def __str__(self):
		d = str(self.latest_submission).split()
		d = d[0] + "_" + d[1].split("+")[0]
		return  self.challenge.challenge_name + "_" + self.group.name + "_" + d

def submission_post_save(sender, instance, **kwargs):

	# Increment the submission count of the challenge submitted to 
	challenge_submitted_to = instance.challenge
	challenge_submitted_to.submission_count += 1
	challenge_submitted_to.save()
post_save.connect(submission_post_save, sender=Submission)

def submission_pre_delete(sender, instance, **kwargs):
	# Decrement the submission count of the challenge that was submitted to
	challenge_submitted_to = instance.challenge
	challenge_submitted_to.submission_count -= 1
	challenge_submitted_to.save()
pre_delete.connect(submission_pre_delete, sender=Submission)

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
