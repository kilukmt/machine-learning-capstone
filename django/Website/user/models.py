from Website import default_images as default
from django.db import models

class Group(models.Model):
	name = models.CharField(max_length=100)

class User(models.Model):
	name = models.CharField(max_length=100)
	password = models.CharField(max_length=100, default="")
	email = models.CharField(max_length=50)
	grad_year = models.IntegerField(default=0)
	groups = models.ManyToManyField(Group)
	user_picture = models.ImageField(upload_to='Images/', default='Images/default_user.jpg')