import os

for file in os.listdir('.'):
	if '1_' in file:
		file_name = file.split('.')[0]
		_, id1, id2 = file_name.split('_')
		os.rename(file, '{}_{}_{}.jpg'.format(2, id1, id2))