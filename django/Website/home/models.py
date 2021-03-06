from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage as FSS

ps = FSS(location=(settings.MEDIA_ROOT + '\\images\\test_images\\'))

class Picture(models.Model):
	u = models.ForeignKey('user.User', on_delete=models.CASCADE, default=1)
	pic = models.ImageField(storage=ps, max_length=300, default='\\images\\default.jpg')
