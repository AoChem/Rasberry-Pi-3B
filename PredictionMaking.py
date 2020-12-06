import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog

import os
import time

def initialization():
	global NameOfSts
	global NumOfSts
	NameOfSts = []
	NumOfSts = tk.simpledialog.askinteger("Initializing", "Input the number of states",
		parent=p,minvalue=1, maxvalue=3)

	if NumOfSts>=1:
		NameOfSts1 = tk.simpledialog.askstring("Initializing", "State1 Name:", parent=p)
		NameOfSts.append(NameOfSts1)
		if NumOfSts>=2:
			NameOfSts2 = tk.simpledialog.askstring("Initializing", "State2 Name:", parent=p)
			NameOfSts.append(NameOfSts2)
			if NumOfSts==3:
				NameOfSts3 = tk.simpledialog.askstring("Initializing", "State3 Name:", parent=p)
				NameOfSts.append(NameOfSts3)

def prediction_making():
	from edgetpu.classification.engine import ClassificationEngine
	from imutils.video import VideoStream
	from PIL import Image
	import imutils
	import cv2
	import ModelTraining
	import SupplementaryPictureTaking

	print("[INFO] parsing class labels...")
	labels = {}

	label_txt = filedialog.askopenfilename(initialdir = "/",title = "Select Label File:",
		filetypes = (("text files","*.txt"),("all files","*.*")))

	# loop over the class labels file
	for row in open(label_txt):
		# unpack the row and update the labels dictionary
		(classID, label) = row.strip().split(" ", maxsplit=1)
		label = label.strip().split(",", maxsplit=1)[0]
		labels[int(classID)] = label

	model_tflite = filedialog.askopenfilename(initialdir = "/",title = "Select Model:",
		filetypes = (("tensor flow lite files:","*.tflite"),("all files","*.*")))

	print("[INFO] loading Coral model...")
	model = ClassificationEngine(model_tflite)

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
			if score >= 0.5:
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
		picture_taking()
		model_training_main()
		ans = input('Would you like to continue classifying video? (y/n)\n')
		if ans == 'y':
			prediction_making()
		else:
			break


p = tk.Tk() # p: parent
p.title('Train Your Own Model')

init_button = tk.Button(p, text='Initialization', width=25, command=initialization).pack()

pm_button = tk.Button(p, text='Make Prediction', width=25, command=prediction_making).pack()

exit_button = tk.Button(p, text='Exit', width=25, command=p.destroy).pack()
p.mainloop()