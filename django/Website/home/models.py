from django.db import models
from user.models import User

class Picture(models.Model):
	user = models.ForeignKey('user.User', on_delete=models.CASCADE, default=1)
	pic = models.ImageField(upload_to='Images/', default='Images/default.jpg')
