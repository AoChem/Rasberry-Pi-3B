from edgetpu.classification.engine import ClassificationEngine
from PIL import Image
import argparse
import imutils
import time
import cv2

def image_classification():
	def check_file_type(image):
		exts = {'.jpg', '.png'}
		file_valid = any(image.endswith(ext) for ext in exts) 
		return file_valid 

	files = os.listdir(os.path.join(path, 'testset'))
	print(files)

	print("[INFO] parsing class labels...")
	labels = {}

	label_txt = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Label File:",
	filetypes=(("text files","*.txt"),("all files","*.*")))
	print(label_txt)

	for row in open(label_txt):
		# unpack the row and update the labels dictionary
		(classID, label) = row.strip().split(" ", maxsplit=1)
		label = label.strip().split(",", maxsplit=1)[0]
		labels[int(classID)] = label

	model_tflite = filedialog.askopenfilename(initialdir=os.getcwd(),title="Select Model:",
		filetypes=(("tensor flow lite files:","*.tflite"),("all files","*.*")))

	print("[INFO] loading Coral model...")
	model = ClassificationEngine(model_tflite)

	output_csv_name = simpledialog.askstring("Image Classifying", "Output results' csv file name:", parent=p)

	# iterate the files in the image folder
	for file in files:
		if check_file_type(file) == False:
			# ignore this file and continue
			print('Invalid Extension')
			continue

		# file_dir -The filredir in local disk
		file_dir = os.path.join(path, 'testset', file)

		# load the input image
		image = cv2.imread(file_dir)
		orig = image.copy()

		# prepare the image for classification by converting (1) it from BGR
		# to RGB channel ordering and then (2) from a NumPy array to PIL
		# image format
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = Image.fromarray(image)

		# make predictions on the input image
		print("[INFO] making predictions...")
		# start = time.time()
		results = model.ClassifyWithImage(image, top_k=5)
		# end = time.time()
		# print("[INFO] classification took {:.4f} seconds...".format(
		# 	end - start))

		# loop over the results
		# for (i, (classID, score)) in enumerate(results):
		# 	# display the classification result to the terminal
		# 	print("{}. {}: {:.2f}%".format(i + 1, labels[classID],
		# 		score * 100))