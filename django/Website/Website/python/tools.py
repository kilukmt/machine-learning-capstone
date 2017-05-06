import os
import datetime
import zipfile
import shutil

from django.conf import settings
from django.db.models import Count
from user.models import User, Group
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
def validate_current_user(session, ID):
	try:
		if (ID == session['user_id']):
			return True
		else:
			return False
	except KeyError:
		return False

def get_session_id(session):
	try:
		id = session['user_id']
	except KeyError:
		return 0

def datetimenow():
	return datetime.datetime.now()

def get_session_groups(session):
	try:
		groups = Group.objects.filter(user=User.objects.get(pk=session['user_id']))
	except KeyError:
		groups = []

	return groups

# Gets a .zip file, unzips it, and validates the format of the filesystem therein
def validate_challenge_files(challenge_files_zip):
	challenge_file_directory = unzip_file(challenge_files_zip)
	challenge_file_directory = validate_unzip(challenge_file_directory)

	# Build path to extracted files directory
	extracted_directory = challenge_files_zip.split(".zip")[0]

	if challenge_file_directory:
		class_num_defs = read_defs(challenge_file_directory)
		if not class_num_defs['error']:
			if valid_file_tree(challenge_file_directory, class_num_defs):
				test_key = build_test_key(challenge_file_directory)
				delete_dir(extracted_directory)
				return (True, test_key)

	delete_dir(extracted_directory)
	return (False, "")

def unzip_file(zip_filepath):
	zip_filename = zip_filepath.split("\\")[-1]
	unzip_file_dir = zip_filepath.split(zip_filename)[0] + zip_filename.split(".zip")[0]
	zip_reader = zipfile.ZipFile(zip_filepath, 'r')
	zip_reader.extractall(unzip_file_dir)
	zip_reader.close()

	return unzip_file_dir

# returns the true directory path of the challenge files being uploaded
# or nothing if the extracted data is invalid
def validate_unzip(extracted_directory):
	dir_items = os.listdir(extracted_directory)
	if len(dir_items) == 1:
		target_dir = extracted_directory + '\\' + dir_items[0]
		if os.path.isdir(target_dir):
			return target_dir

	return ""

def delete_dir(dir_path):
	shutil.rmtree(dir_path)

# validates the format of the "class_num_defs.txt" file
# and returns a dictionary of the entries
def read_defs(challenge_directory):
	try:
		file_reader = open(challenge_directory + '\\class_num_defs.txt')
	except FileNotFoundError:
		return {'error': True }

	class_num_defs = {}

	for line in file_reader:
		(num, name) = line.split(":")
		name = name.split("\n")[0]
		if (not name in class_num_defs) and (not num in class_num_defs.values()):
			class_num_defs[name] = int(num)
		else:
			return {'error': True}

	class_num_defs['error'] = False
	return class_num_defs

def valid_file_tree(challenge_directory, class_num_defs):
	if os.path.isdir(challenge_directory + '\\test'):
		if os.path.isdir(challenge_directory + '\\train'):
			if len(os.listdir(challenge_directory)) == 3:
				if validate_training_dir(challenge_directory, class_num_defs):
					if validate_test_dir(challenge_directory, class_num_defs):
						return True

	return False

def validate_training_dir(challenge_directory, class_num_defs):
	train_dir = challenge_directory + '\\train'
	dir_items = os.listdir(train_dir)

	# examine every directory in the '/train' directory
	for item in dir_items:

		# check if the item in the '/train' directory really is a directory
		if os.path.isdir(train_dir + '\\' + item):
			if item in class_num_defs:

				# Make sure all files in class training directory are images
				class_training_imgs = os.listdir(train_dir + '\\' + item)
				for img in class_training_imgs:
					if not (('.jpg' in img) or ('.png' in img)):
						return False
			else:
				return False
		else:
			return False

	return True

def validate_test_dir(challenge_directory, class_num_defs):
	# Make sure all the items in the test directory are images and that
	# they are formatted correctly with a valid class # leading the filename
	dir_items = os.listdir(challenge_directory + '\\test')
	for item in dir_items:
		if not (('.jpg' in item) or ('.png' in item)):
			return False
		try:
			if not int(item.split("_")[0]) in class_num_defs.values():
				return False
		except ValueError:
			return False

	return True

def build_test_key(challenge_directory):
	test_key = ""
	dir_items = os.listdir(challenge_directory + '\\test')
	for item in dir_items:
		test_key += item.split("_")[0] + ', '

	# Get rid of the last comma and return the key
	return test_key[:-2]
