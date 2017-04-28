import os
import datetime

from django.conf import settings
from user.models import User
from home.models import Picture

def handle_uploaded_file(file):
	return 1

def handle_uploaded_pic(pic, user_id):
	try:
		user = User.objects.get(pk=user_id)
	except DoesNotExist:
		return -1

	img_path = settings.MEDIA_ROOT + 'images\\'
	ldap = user.email.split('@')[0]										# Everything before the '@' in the user's ASU email
																		# e.g email=smithjb@appstate.edu --> ldap=smithjb
	img_path = img_path + ldap + '\\'
	fqpn = img_path + date_time_squish() + '_' + ldap + '.jpg'			# fqpn:fully qualified pathname | for image

	# If the user doesn't have an image directory already,
	# make them and image directory
	if not (image_directory_exists(img_path)):
		os.makedirs(img_path)

	# Write image to fqpn
	with open(fqpn, 'wb+') as destination:
		for chunk in pic.chunks():
			destination.write(chunk)

	# Create picture instance and save it to the database
	pic = Picture(u=(User.objects.get(pk=user_id)), pic=fqpn)
	pic.save()

	# Link the picture instance with the user
	user.picture_set.add(pic)

	# Save user to database
	user.save()

def image_directory_exists(path):
	return (os.path.isdir(path))

def date_time_squish():
	(date, time_segments) = str(datetime.datetime.now()).split()					# length=2
																			# dt is a string in the form: "2017-04-08 00:46:59.697793"
	(hours, mins, secs) = time_segments.split(':')							# length=3
	(secs, millisecs) = secs.split('.')										# breaks up the seconds float
	seconds_squished = secs + millisecs
	s = date + '_' + hours + mins + seconds_squished

	# Should return string in the form: "2017-04-08_004659697793_<ldap>.jpg"
	return s

# Specifically used to check the return value of handle_uploaded_pic
# if num == -1 return false
# else return true
def is_valid(num):
	return not(int(num) < 0)

# Given the ID requested, validate that the user making the request is associated with the ID
def validate_current_user(request, ID):
	try:
		if (ID == request.session['user_id']):
			return True
		else:
			return False
	except KeyError:
		return False
	