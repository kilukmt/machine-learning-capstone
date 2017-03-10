from django.db import models

class Picture(models.Model):
	path = models.CharField(max_length=500)