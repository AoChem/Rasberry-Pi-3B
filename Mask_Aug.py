# Guide of Data Augmentator refers to (Official Documentation)[https://augmentor.readthedocs.io/en/master/userguide/mainfeatures.html]
def augmentdata(imageset_path, imageset_aug_path, label_list):
	import Augmentor
	for label in label_list:
		path_to_image = imageset_path + label + "/"
		output_path = imageset_aug_path + label + "/"
		# path_to_imageset = "images/"
		# label = assembled
		p = Augmentor.Pipeline(source_directory=path_to_image, output_directory=output_path)
		p.rotate(probability=0.5, max_left_rotation=10, \
			max_right_rotation=10)
		p.skew_tilt(probability=0.2, magnitude=0.1)
		p.random_erasing(probability=0.2, rectangle_area=0.2)
		p.random_brightness(probability=0.2, min_factor=0.8, \
			max_factor=0.9)
		p.sample(200)

imageset_aug_path = 'images_augmented/'
imageset_path = 'images/'
label_list = ['w', 'wo']

augmentdata(imageset_path, imageset_aug_path, label_list)
