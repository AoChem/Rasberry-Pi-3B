import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog

import os
import time
# import DatasetImporting as dsi
# import DataAugmentation as da
# import ModelTraining as mt
# import VideoClassification as vc

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
# This code is for importing existed dataset.

# Guide of Data Augmentator refers to (Official Documentation)[https://augmentor.readthedocs.io/en/master/userguide/mainfeatures.html]
def data_augmentation():
	import Augmentor

	def data_augmenting():
		for x in range(NumOfSts):
			NumOfSmp = tk.simpledialog.askinteger("Data Augmenting", "Input the number of samples:",
				parent=da, minvalue=50, maxvalue=500)
			
			SrcPath = tk.filedialog.askdirectory(parent=da,
				initialdir=os.getcwd(),
				title = "Please select the source folder:")
			if SrcPath == "":
				tk.messagebox.showwarning("Warning", "Empty Path!")
				time.sleep(1)
				SrcPath = tk.filedialog.askdirectory()
			else:
				SrcPath.replace('/', '\\')

			DstPath = tk.filedialog.askdirectory(parent=da,
				initialdir=os.getcwd(),
				title = "Please select the destination folder:")
			if SrcPath == "":
				tk.messagebox.showwarning("Warning", "Empty Path!")
				time.sleep(1)
				SrcPath = tk.filedialog.askdirectory()
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

	da = tk.Toplevel()
	da.title('Data Augmenting...')

	var1 = tk.IntVar()
	tk.Checkbutton(da, text='Rotation', variable=var1).pack()
	var2 = tk.IntVar()
	tk.Checkbutton(da, text='Skew & Tilt', variable=var2).pack()
	var3 = tk.IntVar()
	tk.Checkbutton(da, text='Mosaic', variable=var3).pack()
	var4 = tk.IntVar()
	tk.Checkbutton(da, text='Brightness', variable=var4).pack()

	tk.Button(da, text='Augment Data', command=data_augmenting).pack()
	tk.Button(da, text='Finish', command=da.destroy).pack()

	da.mainloop()

# create the parent window
p = tk.Tk() # p: parent
p.title('Train Your Own Model')

init_button = tk.Button(p, text='Initialization', width=25, command=initialization).pack()

da_button = tk.Button(p, text='Augment Data', width=25, command=data_augmentation).pack()

exit_button = tk.Button(p, text='Exit', width=25, command=p.destroy).pack()
p.mainloop()