# This file is for Taking Pictures of different status of a given task

# Create buttons for collecting photos of different status
# package info: https://www.raspberrypi.org/blog/gpio-zero-a-friendly-python-api-for-physical-computing/
from gpiozero import Button 
# Use picamera library to control the camera module of Raspi
from picamera import PiCamera
# gmtime: return the time info
# strftime: accept the time info returned by gmtime
from time import gmtime, strftime

# u: unassembled status
def take_picture_u():
	print("Unassembled Status Picture Taking!")
	output = strftime("/home/pi/AoChenST/StsClsf/images/unassembled/image-%d-%m-%H:%M:%S.png", gmtime())
	camera.capture(output)
# a: asse,bled status
def take_picture_a():
	print("Assembled Status Picture Taking!")
	output = strftime("/home/pi/AoChenST/StsClsf/images/assembled/image-%d-%m-%H:%M:%S.png", gmtime())
	camera.capture(output)

assembled_pic_btn = Button(14)
unassembled_pic_btn = Button(15)

camera = PiCamera()
camera.resolution = (800, 480)

print("Start Status Classification!")
camera.start_preview()

try:
	while True:
		assembled_pic_btn.when_pressed = take_picture_a
		unassembled_pic_btn.when_pressed = take_picture_u
except KeyboardInterrupt:
	pass

camera.stop_preview()
print("\n Stop Status Classification!")
