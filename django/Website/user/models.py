from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage as FSS

ps = FSS(location=(settings.MEDIA_ROOT + 'users\\'))

class Group(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class User(models.Model):
	name = models.CharField(max_length=100)
	password = models.CharField(max_length=100, default="")
	email = models.CharField(max_length=50)
	grad_year = models.IntegerField(default=0)
	groups = models.ManyToManyField(Group)
	user_picture = models.ImageField(storage=ps, max_length=300, default=(ps.location + 'default.jpg'))

	def __str__(self):
		return self.name
		