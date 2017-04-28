from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage as FSS

fs = FSS(location=(settings.MEDIA_ROOT + 'challenges\\'))
ps = FSS(location=(fs.location + '\\challenge_avis\\'))

class Challenge(models.Model):
	challenge_name = models.CharField(max_length=100)
	challenge_description = models.TextField()
	challenge_files = models.FileField(storage=fs, max_length=300, default=(fs.location + '\\default.txt'))
	date_created = models.DateTimeField('date created')
	challenge_image = models.ImageField(storage=ps, max_length=300, default=(ps.location + '\\default.jpg'))

	def __str__(self):
		return self.challenge_name

class Submission(models.Model):
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, default=1)
	group  = models.ForeignKey('user.Group', on_delete=models.CASCADE, default=1)
	error_rate = models.DecimalField(max_digits=3, decimal_places=3)

class HelpComment(models.Model):
	challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, default=1)
	user = models.ForeignKey('user.User', on_delete=models.CASCADE, default=1)
	comment_replied_to = models.ForeignKey('self', on_delete=models.CASCADE, default=1)
	comment_text = models.TextField()
	date = models.DateTimeField('date written')
	up_votes = models.IntegerField(default=0)
	down_votes = models.IntegerField(default=0)
	pictures = models.ManyToManyField('home.Picture')

