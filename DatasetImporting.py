# This code is for importing existed dataset.
def dataset_importing(NumOfSts, NameOfSts):
	import shutil

	for x in range(NumOfSts):
		print("Please input "+NameOfSts[x]+\
			" dataset's path on your computer:\n")
		source_dataset_path = input()
		# sample:'~/AoChenST/.../dataset/with_mask/'
		destination_path = '/home/pi/AoChenST/StsClsf/images/'\
			+NameOfSts[x]+'/'
		shutil.copy(source_dataset_path, destination_path)

	print('Dataset importing finished.')
