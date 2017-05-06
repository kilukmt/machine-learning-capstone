import zipfile

def unzip_file(zip_filepath):
	zip_filename = zip_filepath.split("\\")[-1]
	zip_file_dir = zip_filepath.split(zip_filename)[0] + "TEMP_" + zip_filename.split(".zip")[0]
	zip_reader = zipfile.ZipFile(zip_filepath, 'r')
	zip_reader.extractall(zip_file_dir)
	zip_reader.close()