# Control Script
import PictureTaking
import DatasetImporting
import DataAugmentation
import ModelTraining
import VideoClassification
import GUICreation

print('Please input the number of states you want to\
	 classify:\n')
NumOfSts = input()
# interger and maximum

NameOfSts = []
for x in range(NumOfSts):
	print('Please input the name of Status' + str(x) + ':\n')
	NameOfSts[x] = input()

print('Would you like to take pictures now? (y/n)\n')
ans1 = input()
if ans1 == 'y':
	PictureTaking.picture_taking(NumOfSts=NumOfSts, \
		NameOfSts=NameOfSts)
else:
	print('No Pictures Taken!')

print('Would you like to import existed dataset? (y/n)\n')
ans2 = input()
if ans2 == 'y':
	DatasetImporting.dataset_importing(NumOfSts=NumOfSts, \
		NameOfSts=NameOfSts)
else:
	print('No Dataset Imported!')

print('Would you like to augment data? (y/n)\n')
ans3 = input()
imageset_path = '/home/pi/AoChenST/StsClsf/images/'\
				+NameOfSts[x]+'/'
aug_imageset_path = '/home/pi/AoChenST/StsClsf/aug_images/'\
				+NameOfSts[x]+'/'
if ans3 == 'y':
	DataAugmentation.data_augmentation(imageset_path=imageset_path, \
		aug_imageset_path=aug_imageset_path, \
		label_list=NameOfSts)
else:
	print('No Data Augmented!')

print('Would you like to train the model now? (y/n)\n')
ans4 = input()
if ans4 == 'y':
	ModelTraining.model_training(NameOfSts)
else:
	print('No Model Trained!')

ans5 = input('Would you like to make predictions now? (y/n)\n')
if ans5 == 'y':
	VideoClassification.video_classification(NameOfSts=NameOfSts)
else:
	print('No Classification Made!')