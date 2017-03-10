from django.db import models

class Group(models.Model):
	name = models.CharField(max_length=100)
	group_picture = models.OneToOneField('home.Picture', default="", on_delete=models.SET_DEFAULT)

class User(models.Model):
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=50)
	grad_year = models.IntegerField(default=0)
	groups = models.ManyToManyField(Group)
	user_picture = models.OneToOneField('home.Picture', default="", on_delete=models.SET_DEFAULT)
