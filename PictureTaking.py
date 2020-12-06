# This file is for Taking Pictures of different status of a given task

# Create buttons for collecting photos of different status
# package info: https://www.raspberrypi.org/blog/gpio-zero-a-friendly-python-api-for-physical-computing/
	
def picture_taking(NumOfSts, NameOfSts):

	from gpiozero import Button 
	# Use picamera library to control the camera module of Raspi
	from picamera import PiCamera
	# gmtime: return the time info
	# strftime: accept the time info returned by gmtime
	from time import gmtime, strftime
	import os

	for x in range(NumOfSts):
		if not os.path.exists('/home/pi/AoChenST/StsClsf/images/'\
			+NameOfSts[x]+'/'):
			os.makedirs('/home/pi/AoChenST/StsClsf/images/'\
				+NameOfSts[x]+'/')

	# 1st Status
	def take_picture_1():
		print("1st Status Picture Taking!")
				output = strftime("/home/pi/AoChenST/StsClsf/images/"\
			+NameOfSts[1]+"/image-%d-%m-%H:%M:%S.png", gmtime())
		camera.capture(output)
	# 2nd Status
	def take_picture_2():
		print("2nd Status Picture Taking!")
		output = strftime("/home/pi/AoChenST/StsClsf/images/"\
			+NameOfSts[2]+"/image-%d-%m-%H:%M:%S.png", gmtime())
		camera.capture(output)
	# 3rd Status
	def take_picture_3():
		print("3rd Status Picture Taking!")
		output = strftime("/home/pi/AoChenST/StsClsf/images/"\
			+NameOfSts[3]+"/image-%d-%m-%H:%M:%S.png", gmtime())
		camera.capture(output)

	PicBtn1 = Button(14)
	PicBtn2 = Button(15)
	# PicBtn3 = 0

	camera = PiCamera()
	camera.resolution = (800, 480)

	print("Start Taking Pictures!\n")
	print("Use Ctrl+C to Quit!\n")

	camera.start_preview()

	try:
		while True:
			PicBtn1.when_pressed = take_picture_1()
			PicBtn2.when_pressed = take_picture_2()
			# PicBtn3.when_pressed = take_picture_3()
	except KeyboardInterrupt:
		pass

	camera.stop_preview()
	print("Stop Taking Pictures!\n")