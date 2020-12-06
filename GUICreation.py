from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog

import os
import time
import keyboard

from google.cloud import storage
from google.cloud import automl
# import DatasetImporting as dsi
# import DataAugmentation as da
# import ModelTraining as mt
# import VideoClassification as vc

def initialization():
	global NameOfSts
	global NumOfSts
	NameOfSts = []
	NumOfSts = simpledialog.askinteger("Initializing", "Input the number of states",
		parent=p,minvalue=1, maxvalue=3)

	if NumOfSts>=1:
		NameOfSts1 = simpledialog.askstring("Initializing", "State1 Name:", parent=p)
		NameOfSts.append(NameOfSts1)
		if NumOfSts>=2:
			NameOfSts2 = simpledialog.askstring("Initializing", "State2 Name:", parent=p)
			NameOfSts.append(NameOfSts2)
			if NumOfSts==3:
				NameOfSts3 = simpledialog.askstring("Initializing", "State3 Name:", parent=p)
				NameOfSts.append(NameOfSts3)

def picture_taking():

def dataset_importing():
	import shutil
	for x in range(NumOfSts):
		source_dataset_path = filedialog.askdirectory(parent=p, initialdir=os.getcwd(),
			title="Please select the folder where the dataset locates:")
		destination_path = filedialog.askdirectory(parent=p, initialdir=os.getcwd(),
			title="Please select the folder you want to import:")
		shutil.copytree(src=source_dataset_path, dst=destination_path, dirs_exist_ok=True)

def data_augmentation():
	import Augmentor

	def data_augmenting():
		for x in range(NumOfSts):
			NumOfSmp = simpledialog.askinteger("Data Augmenting", "Input the number of samples:",
				parent=da, minvalue=50, maxvalue=500)
			
			SrcPath = filedialog.askdirectory(parent=da,
				initialdir=os.getcwd(),
				title = "Please select the source folder:")
			if SrcPath == "":
				messagebox.showwarning("Warning", "Empty Path!")
				time.sleep(1)
				SrcPath = filedialog.askdirectory()
			else:
				SrcPath.replace('/', '\\')

			DstPath = filedialog.askdirectory(parent=da,
				initialdir=os.getcwd(),
				title = "Please select the destination folder:")
			if SrcPath == "":
				messagebox.showwarning("Warning", "Empty Path!")
				time.sleep(1)
				SrcPath = filedialog.askdirectory()
			else:
				SrcPath.replace('/', '\\')

			pl = Augmentor.Pipeline(source_directory=SrcPath,\
				output_directory=DstPath)

			if var1.get() == 1:
				pl.rotate(probability=0.5, max_left_rotation=10, \
					max_right_rotation=10)
			if var2.get() == 1:
				pl.skew_tilt(probability=0.2, magnitude=0.1)
			if var3.get() == 1:
				pl.random_erasing(probability=0.2, rectangle_area=0.2)
			if var4.get() == 1:
				pl.random_brightness(probability=0.2, min_factor=0.8, \
					max_factor=0.9)
			
			pl.sample(NumOfSmp)

	da = Toplevel()
	da.title('Data Augmenting...')

	var1 = IntVar()
	Checkbutton(da, text='Rotation', variable=var1).pack()
	var2 = IntVar()
	Checkbutton(da, text='Skew & Tilt', variable=var2).pack()
	var3 = IntVar()
	Checkbutton(da, text='Mosaic', variable=var3).pack()
	var4 = IntVar()
	Checkbutton(da, text='Brightness', variable=var4).pack()

	Button(da, text='Augment Data', command=data_augmenting).pack()
	Button(da, text='Finish', command=da.destroy).pack()

	da.mainloop()

def model_training_main():
	def model_training_init(parent):
		# why run before clicking??????
		mt = parent
		global display_name, model_name, model_filename, csv_name
		display_name = simpledialog.askstring("Initializing", "Dataset Name:", parent=mt)
		model_name = simpledialog.askstring("Initializing", "Model Name on Google Cloud Storage:", parent=mt)
		model_filename = simpledialog.askstring("Initializing", "Model Name on Local Device:", parent=mt)
		csv_name = simpledialog.askstring("Initializing", "*.csv File Name:", parent=mt)

	def dataset_selecting(parent):
		mt = parent
		global image_path
		image_path = filedialog.askdirectory(parent=mt, initialdir=os.getcwd(),
			title="Please select the dataset you want to train:")

	def model_training(display_name, model_name, model_filename, csv_name):
		from ImageUploading import upload_image_excel # self_defined
		from dotenv import load_dotenv
		load_dotenv()

		# set up google cloud automl 
		project_id = os.getenv("PROJECT_ID")
		bucket_name = os.getenv("BUCKET_NAME")
		remote_model_filename = 'edgetpu_model.tflite' #tflite: TensorFlow Lite
		model_format = 'edgetpu_tflite'
		train_budget = 12000 # budget/1000 equals 1 node hour
		storage_client = storage.Client()
		client = automl.AutoMlClient()
		project_location = f"projects/{project_id}/locations/us-central1"
		bucket = storage_client.bucket(bucket_name)
		display_name=display_name
		model_name=model_name
		model_filename=model_filename
		csv_name=csv_name

		#----------------------Create an empty dataset----------------------

		print('Dataset Creation...')
		metadata = automl.ImageClassificationDatasetMetadata(
		    classification_type=automl.ClassificationType.MULTICLASS
		)
		dataset = automl.Dataset(
		    display_name=display_name,
		    image_classification_dataset_metadata=metadata
		)

		# Create a dataset with the dataset metadata in the region.
		response = client.create_dataset(parent=project_location, dataset=dataset)
		created_dataset = response.result()
		# Display the dataset information
		print("Dataset name: {}".format(created_dataset.name))
		print("Dataset id: {}".format(created_dataset.name.split("/")[-1]))
		dataset_id = created_dataset.name.split("/")[-1]

		#--------------Upload the images to google cloud bucket and create a *.csv file-------------
		print("Uploading Images...")
		status_list = NameOfSts
		upload_image_excel(bucket, bucket_name, display_name, image_path, status_list, csv_name)

		#----------------------Import the images to created dataset---------------------------------
		print("Importing Images...")
		# Read the *.csv file on Google Cloud
		remote_csv_path = 'gs://{0}/{1}'.format(bucket_name, csv_name)
		# Get the full path of the dataset.
		dataset_full_id = client.dataset_path(
		    project_id, "us-central1", dataset_id
		)

		# Get the multiple Google Cloud Storage URIs
		# A Uniform Resource Identifier (URI) is a string of characters that unambiguously identifies a particular resource.
		input_uris = remote_csv_path.split(",")
		gcs_source = automl.GcsSource(input_uris=input_uris)
		input_config = automl.InputConfig(gcs_source=gcs_source)

		# Import data from the input URI
		response = client.import_data(name=dataset_full_id, input_config=input_config)

		print("Data imported. {}".format(response.result()))

		#-----------------Create and Train the Model-----------------------------------
		model_metadata = automl.ImageClassificationModelMetadata(
			train_budget_milli_node_hours=train_budget,
			model_type="mobile-high-accuracy-1"
		)
		model = automl.Model(
			display_name=model_name,
			dataset_id=dataset_id,
			image_classification_model_metadata = model_metadata,
		)

		# Create a model with the model metadata in the region.
		response = client.create_model(parent=project_location, model=model)

		print("Training operation name: {}".format(response.operation.name))
		print("Training started...")

		created_model = response.result()
		# Display the dataset information
		print("Model name: {}".format(created_model.name))
		print("Model id: {}".format(created_model.name.split("/")[-1]))

		#--------------------Listing Models--------------------------------
		request = automl.ListModelsRequest(parent=project_location, filter="")
		response = client.list_models(request=request)

		export_configuration = {
			'model_format': model_format,
			'gcs_destination':{'output_uri_prefix': 'gs://{}/'.format(bucket_name)}
		}

		for model in response:
			# check models in project and export new one
			if model.display_name == model_name:
				# export model to bucket
				model_full_id = client.model_path(project_id, "us-central1", model.name.split("/")[-1])
				response = client.export_model(name=model_full_id, output_config=export_configuration)

		# get information on model storage location and download it to local directory "models"
		export_metadata = response.metadata
		export_directory = export_metadata.export_model_details.output_info.gcs_output_directory
		print(export_metadata)
		print(export_directory)

		model_dir_remote = export_directory + remote_model_filename
		model_dir = os.path.join("models", model_filename) 
		print(model_dir_remote)
		print(model_dir)

		# wait for model to be exported
		blob1 = bucket.blob(model_dir_remote)
		blob1.download_to_filename(model_dir)

		print("Process completed, new model is now accessible locally.")

	# set up authentication credentials
	print("Initializing...")

	mt = Toplevel()
	mt.title("Model Training...")

	para_init_button = Button(mt, text='Initializing Parameters...', command=model_training_init(mt)).pack()
	select_button = Button(mt, text='Select Dataset...', command=dataset_selecting(mt)).pack()
	train_button = Button(mt, text='Train', command=model_training(display_name, model_name, model_filename, csv_name)).pack()
	exit_button = Button(mt, text='Exit', command=mt.destroy).pack()

	mt.mainloop()

def prediction_making():
	from edgetpu.classification.engine import ClassificationEngine
	from imutils.video import VideoStream
	from PIL import Image
	import imutils
	import cv2

	print("[INFO] parsing class labels...")
	labels = {}

	label_txt = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Label File:",
		filetypes=(("text files","*.txt"),("all files","*.*")))
	print(label_txt)

	# loop over the class labels file
	for row in open(label_txt):
		# unpack the row and update the labels dictionary
		(classID, label) = row.strip().split(" ", maxsplit=1)
		label = label.strip().split(",", maxsplit=1)[0]
		labels[int(classID)] = label

	model_tflite = filedialog.askopenfilename(initialdir=os.getcwd(),title="Select Model:",
		filetypes=(("tensor flow lite files:","*.tflite"),("all files","*.*")))

	print("[INFO] loading Coral model...")
	model = ClassificationEngine(model_tflite)

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

		color = (0, 0, 255)
		# ensure at least one result was found
		if len(results) > 0:
			# draw the predicted class label, probability, and inference
			# time on the output frame
			(classID, score) = results[0]
			text = "{}: {:.2f}% ({:.4f} sec)".format(labels[classID],
				score * 100, end - start)
			if score >= 0.7:
				if classID == 1:
					color = (0, 255, 0)
				cv2.putText(orig, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
					0.5, color, 2)

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

# create the parent window
p = Tk() # p: parent
p.title('Train Your Own Model')

init_button = Button(p, text='Initialization', width=25, command=initialization).pack()

pt_button = Button(p, text='Take Pictures', width=25, command=picture_taking).pack()

dsi_button = Button(p, text='Import Dataset', width=25, command=dataset_importing).pack()

da_button = Button(p, text='Augment Data', width=25, command=data_augmentation).pack()

mt_button = Button(p, text='Train Model', width=25, command=model_training_main).pack()

pm_button = Button(p, text='Make Prediction', width=25, command=prediction_making).pack()

exit_button = Button(p, text='Exit', width=25, command=p.destroy).pack()

p.mainloop()