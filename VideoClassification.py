# USAGE
# python classify_video.py --model mobilenet_v2/mobilenet_v2_1.0_224_quant_edgetpu.tflite --labels mobilenet_v2/imagenet_labels.txt

# import the necessary packages
from edgetpu.classification.engine import ClassificationEngine
from imutils.video import VideoStream
from PIL import Image
import argparse
import imutils
import time
import cv2
import ModelTraining
import SupplementaryPictureTaking

def video_classification(NameOfSts):
	

	# construct the argument parser and parse the arguments
	# ap = argparse.ArgumentParser()
	# ap.add_argument("-m", "--model", required=True,
	# 	help="path to TensorFlow Lite classification model")
	# ap.add_argument("-l", "--labels", required=True,
	# 	help="path to labels file")
	# args = vars(ap.parse_args())

	# initialize the labels dictionary
	print("[INFO] parsing class labels...")
	labels = {}

	# loop over the class labels file
	for row in open(input('Please input the path of lables text file:')):
		# unpack the row and update the labels dictionary
		(classID, label) = row.strip().split(" ", maxsplit=1)
		label = label.strip().split(",", maxsplit=1)[0]
		labels[int(classID)] = label

	# load the Google Coral classification model
	print("[INFO] loading Coral model...")
	model = ClassificationEngine(input('Please input the path of model you want to deploy:')])

	# initialize the video stream and allow the camera sensor to warmup
	print("[INFO] starting video stream...")
	vs = VideoStream(src=0).start()
	#vs = VideoStream(usePiCamera=False).start()
	time.sleep(2.0)

	print('[INFO] press `q` to quit the classification mode')
	print('[INFO] press `t` to enter the training mode')
	training = False
	# loop over the frames from the video stream
	while True:
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 500 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=500)
		orig = frame.copy()

		# prepare the frame for classification by converting (1) it from
		# BGR to RGB channel ordering and then (2) from a NumPy array to
		# PIL image format
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		frame = Image.fromarray(frame)

		# make predictions on the input frame
		start = time.time()
		results = model.classify_with_image(frame, top_k=1)
		end = time.time()

		# ensure at least one result was found
		if len(results) > 0:
			# draw the predicted class label, probability, and inference
			# time on the output frame
			(classID, score) = results[0]
			text = "{}: {:.2f}% ({:.4f} sec)".format(labels[classID],
				score * 100, end - start)
			if score >= 0.8:
				cv2.putText(orig, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
					0.5, (0, 0, 255), 2)

		# show the output frame and wait for a key press
		cv2.imshow("Frame", orig)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord('q'):
			break

		# if the `t` key was pressed, change to the training mode
		if key == ord('t'):
			training = True
			break

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()

	while training:
		print('Training Mode!')
		SupplementaryPictureTaking.picture_taking(NameOfSts)
		ModelTraining.model_training(NameOfSts)
		ans = input('Would you like to continue classifying video? (y/n)\n')
		if ans == 'y':
			video_classification(NameOfSts)
		else:
			break