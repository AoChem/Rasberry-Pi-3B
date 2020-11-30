# This file is for Taking Pictures of different status of a given task

# Create buttons for collecting photos of different status
# package info: https://www.raspberrypi.org/blog/gpio-zero-a-friendly-python-api-for-physical-computing/
from gpiozero import Button 
# Use picamera library to control the camera module of Raspi
from picamera import PiCamera
# gmtime: return the time info
# strftime: accept the time info returned by gmtime, it returns a string representing data and time
from time import gmtime, strftime

# u: unassembled status
def take_picture_u():
	global idx
	print("Unassembled Status Picture Token!")
	output = "/home/pi/AoChenST/StsClsf/img4prd/una{}.png".format(str(idx))
	idx += 1
	camera.capture(output)
# a: assembled status
def take_picture_a():
	global idx
	print("Assembled Status Picture Token!")
	output = "/home/pi/AoChenST/StsClsf/img4prd/a{}.png".format(str(idx))
	idx += 1
	camera.capture(output)

assembled_pic_btn = Button(14)
unassembled_pic_btn = Button(15)

camera = PiCamera()
camera.resolution = (800, 480)

print("Start Taking Pictures for Prediction!")
camera.start_preview()

idx = 0

try:
	while True:
		assembled_pic_btn.when_pressed = take_picture_a
		unassembled_pic_btn.when_pressed = take_picture_u

except KeyboardInterrupt:
	pass

camera.stop_preview()
print("\n Stop Taking Pictures for Prediction!")
