# This code is for Uploading Data, Training Model on Google Cloud, 
# and Downloading the model to Raspi 
def model_training(NameOfSts):
	from dotenv import load_dotenv
	load_dotenv()

	import os
	import time
	from google.cloud import storage
	from google.cloud import automl
	from ImageUploading import upload_image_excel # self_defined

	# set up google cloud automl 
	project_id = input('Please input the project id on Google Cloud Storage:')
	display_name = input('Please name the dataset:') # dataset name
	storage_client = storage.Client()
	bucket_name = input('Please input the bucket name on Google Cloud Storage:')
	model_name = input('Please name your model on Google Cloud Storage:')
	remote_model_filename = 'edgetpu_model.tflite' #tflite: TensorFlow Lite
	model_filename = input('Please name your model on your local device:')
	csv_name = input('Please name the *.csv file which stores data information:')
	model_format = 'edgetpu_tflite'
	train_budget = 12000 # budget/1000 equals 1 node hour

	# set up authentication credentials
	print("Authentication...")

	client = automl.AutoMlClient()
	project_location = f"projects/{project_id}/locations/us-central1"
	bucket = storage_client.bucket(bucket_name)

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
	upload_image_excel(bucket, bucket_name, display_name, status_list, csv_name)

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
	blob = bucket.blob(model_dir_remote)
	blob.download_to_filename(model_dir)

	print("Process completed, new model is now accessible locally.")