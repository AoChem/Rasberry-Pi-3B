from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog

import os
import time

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

	# # def model_training(display_name, model_name, model_filename, csv_name):
	# 	from ImageUploading import upload_image_excel # self_defined
	# 	from dotenv import load_dotenv
	# 	load_dotenv()

	# 	# set up google cloud automl 
	# 	project_id = os.getenv("PROJECT_ID")
	# 	bucket_name = os.getenv("BUCKET_NAME")
	# 	remote_model_filename = 'edgetpu_model.tflite' #tflite: TensorFlow Lite
	# 	model_format = 'edgetpu_tflite'
	# 	train_budget = 12000 # budget/1000 equals 1 node hour
	# 	storage_client = storage.Client()
	# 	client = automl.AutoMlClient()
	# 	project_location = f"projects/{project_id}/locations/us-central1"
	# 	bucket = storage_client.bucket(bucket_name)
	# 	display_name=display_name
	# 	model_name=model_name
	# 	model_filename=model_filename
	# 	csv_name=csv_name

	# 	#----------------------Create an empty dataset----------------------

	# 	print('Dataset Creation...')
	# 	metadata = automl.ImageClassificationDatasetMetadata(
	# 	    classification_type=automl.ClassificationType.MULTICLASS
	# 	)
	# 	dataset = automl.Dataset(
	# 	    display_name=display_name,
	# 	    image_classification_dataset_metadata=metadata
	# 	)

	# 	# Create a dataset with the dataset metadata in the region.
	# 	response = client.create_dataset(parent=project_location, dataset=dataset)
	# 	created_dataset = response.result()
	# 	# Display the dataset information
	# 	print("Dataset name: {}".format(created_dataset.name))
	# 	print("Dataset id: {}".format(created_dataset.name.split("/")[-1]))
	# 	dataset_id = created_dataset.name.split("/")[-1]

	# 	#--------------Upload the images to google cloud bucket and create a *.csv file-------------
	# 	print("Uploading Images...")
	# 	status_list = NameOfSts
	# 	upload_image_excel(bucket, bucket_name, display_name, image_path, status_list, csv_name)

	# 	#----------------------Import the images to created dataset---------------------------------
	# 	print("Importing Images...")
	# 	# Read the *.csv file on Google Cloud
	# 	remote_csv_path = 'gs://{0}/{1}'.format(bucket_name, csv_name)
	# 	# Get the full path of the dataset.
	# 	dataset_full_id = client.dataset_path(
	# 	    project_id, "us-central1", dataset_id
	# 	)

	# 	# Get the multiple Google Cloud Storage URIs
	# 	# A Uniform Resource Identifier (URI) is a string of characters that unambiguously identifies a particular resource.
	# 	input_uris = remote_csv_path.split(",")
	# 	gcs_source = automl.GcsSource(input_uris=input_uris)
	# 	input_config = automl.InputConfig(gcs_source=gcs_source)

	# 	# Import data from the input URI
	# 	response = client.import_data(name=dataset_full_id, input_config=input_config)

	# 	print("Data imported. {}".format(response.result()))

	# 	#-----------------Create and Train the Model-----------------------------------
	# 	model_metadata = automl.ImageClassificationModelMetadata(
	# 		train_budget_milli_node_hours=train_budget,
	# 		model_type="mobile-high-accuracy-1"
	# 	)
	# 	model = automl.Model(
	# 		display_name=model_name,
	# 		dataset_id=dataset_id,
	# 		image_classification_model_metadata = model_metadata,
	# 	)

	# 	# Create a model with the model metadata in the region.
	# 	response = client.create_model(parent=project_location, model=model)

	# 	print("Training operation name: {}".format(response.operation.name))
	# 	print("Training started...")

	# 	created_model = response.result()
	# 	# Display the dataset information
	# 	print("Model name: {}".format(created_model.name))
	# 	print("Model id: {}".format(created_model.name.split("/")[-1]))

	# 	#--------------------Listing Models--------------------------------
	# 	request = automl.ListModelsRequest(parent=project_location, filter="")
	# 	response = client.list_models(request=request)

	# 	export_configuration = {
	# 		'model_format': model_format,
	# 		'gcs_destination':{'output_uri_prefix': 'gs://{}/'.format(bucket_name)}
	# 	}

	# 	for model in response:
	# 		# check models in project and export new one
	# 		if model.display_name == model_name:
	# 			# export model to bucket
	# 			model_full_id = client.model_path(project_id, "us-central1", model.name.split("/")[-1])
	# 			response = client.export_model(name=model_full_id, output_config=export_configuration)

	# 	# get information on model storage location and download it to local directory "models"
	# 	export_metadata = response.metadata
	# 	export_directory = export_metadata.export_model_details.output_info.gcs_output_directory
	# 	print(export_metadata)
	# 	print(export_directory)

	# 	model_dir_remote = export_directory + remote_model_filename
	# 	model_dir = os.path.join("models", model_filename) 
	# 	print(model_dir_remote)
	# 	print(model_dir)

	# 	# wait for model to be exported
	# 	blob1 = bucket.blob(model_dir_remote)
	# 	blob1.download_to_filename(model_dir)

	# 	print("Process completed, new model is now accessible locally.")

	# set up authentication credentials
	print("Initializing...")

	mt = Toplevel()
	mt.title("Model Training...")

	para_init_button = Button(mt, text='Initializing Parameters...', command=model_training_init(mt)).pack()
	select_button = Button(mt, text='Select Dataset...', command=dataset_selecting(mt)).pack()
	print(display_name, type(display_name), model_name, type(model_name),
		model_filename, type(model_filename), csv_name, type(csv_name), type(image_path))
	# train_button = Button(mt, text='Train', command=model_training(display_name, model_name, model_filename, csv_name)).pack()
	exit_button = Button(mt, text='Exit', command=mt.destroy).pack()

	mt.mainloop()

# tkinter.entry try
	# Label(mt, text='Dataset Name').grid(row=0)
	# Label(mt, text='Model Name on Google Cloud Storage').grid(row=1)
	# Label(mt, text='Model Name on Local Device').grid(row=2)
	# Label(mt, text='*.csv File Name').grid(row=3)

	# e1 = Entry(mt)
	# e1.grid(row=0, column=1)
	# e2 = Entry(mt)
	# e2.grid(row=1, column=1)
	# e3 = Entry(mt)
	# e3.grid(row=2, column=1)
	# e4 = Entry(mt)
	# e4.grid(row=3, column=1)
	# display_name = e1.get()
	# model_name = e2.get()
	# model_filename = e3.get()
	# csv_name = e4.get()

# create the parent window
p = Tk() # p: parent
p.title('Train Your Own Model')

init_button = Button(p, text='Initialization', width=25, command=initialization).pack()

mt_button = Button(p, text='Train Model', width=25, command=model_training_main).pack()

exit_button = Button(p, text='Exit', width=25, command=p.destroy).pack()

p.mainloop()