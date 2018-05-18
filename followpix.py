import subprocess
import os
from pixy import *
from ctypes import *
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Initialize Pixy Interpreter thread #
pixy_init()

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

blocks = BlockArray(100)
frame  = 0

# ****************************************************
# Motor Controller Pins
# ****************************************************
freq = 100
A = 26
A_a = 10
A_b = 12
B = 22
B_a = 16
B_b = 18 
C = 24
C_a = 38
C_b = 40

purple = 31
white = 23

GPIO.setup(A, GPIO.OUT)
GPIO.setup(A_a, GPIO.OUT)
GPIO.setup(A_b, GPIO.OUT)

GPIO.setup(B, GPIO.OUT)
GPIO.setup(B_a, GPIO.OUT)
GPIO.setup(B_b, GPIO.OUT)

GPIO.setup(C, GPIO.OUT)
GPIO.setup(C_a, GPIO.OUT)
GPIO.setup(C_b, GPIO.OUT)

GPIO.setup(purple, GPIO.OUT)
GPIO.setup(white, GPIO.OUT)

pwmA = GPIO.PWM(A, 100)
pwmB = GPIO.PWM(B, 100)
pwmC = GPIO.PWM(C, 100)

GPIO.output(A, True)
GPIO.output(B, True)
GPIO.output(C, True)

GPIO.output(purple, False)
GPIO.output(white, False)


# ****************************************************
# Sensor Pins
# ****************************************************
TrigU1 = 11
EchoU1 = 21
ButtonSwitch = 33

GPIO.setup(ButtonSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(TrigU1, GPIO.OUT)
GPIO.output(TrigU1, False)
GPIO.setup(EchoU1, GPIO.IN)


# Globals
sideStep = 0.33; # Limiting factor to ensure direct side to side movement

# ****************************************************
# Set A motor direction
# ****************************************************
def aDir(dir):
	GPIO.output(A_a, dir)
	GPIO.output(A_b, (not dir))
	
# ****************************************************
# Set B motor direction
# ****************************************************
def bDir(dir):
	GPIO.output(B_a, dir)
	GPIO.output(B_b, (not dir))

# ****************************************************
# Set C motor direction
# ****************************************************
def cDir(dir):
	GPIO.output(C_a, dir)
	GPIO.output(C_b, (not dir))

# ****************************************************
# Stops the motors
# RETURNS: none
# ****************************************************
def allStop():
	pwmA.stop()
	pwmB.stop()
	pwmC.stop()


def distance():
	while GPIO.input(EchoU1) == 0:
		pass
	start = time.time()

	while GPIO.input(EchoU1) == 1:
		pass
	stop = time.time()

	dist = (stop-start) * 17150
	return dist

print("Starting follow me mode...")

# set directions
aDir(True)
bDir(True)
cDir(True)
# start motors
pwmA.start(A)
pwmB.start(B)
pwmC.start(C)

SET_DIST = 80 #cm
kp = 5

spinSpeed = 80
speed = 50
sidespeed = 0

pwmA.ChangeDutyCycle(65)
pwmB.ChangeDutyCycle(65)
pwmC.ChangeDutyCycle(65)


while True:
	count = pixy_get_blocks(100, blocks)
	print(count)
	if (count > 0):
		break
	
print("found")
while True:
	time.sleep(0.1)
	GPIO.output(TrigU1, True)
	time.sleep(0.0001)
	GPIO.output(TrigU1, False)

	while GPIO.input(EchoU1) == 0:
		pass
	start = time.time()

	while GPIO.input(EchoU1) == 1:
		pass
	stop = time.time()

	dist = (stop-start) * 17150
	currdist = dist
	print(str(currdist) + "cm")
	
	if currdist > 1:
		count = pixy_get_blocks(100, blocks)
		if (count > 0):
			xavg = 0
			for index in range (0, count):
				xavg += int(blocks[index].x)
				#print('[X=%3d Y=%3d]' % (blocks[index].x, blocks[index].y))
			xavg = xavg / count
			#print("xavg: " + str(xavg))
			if (xavg < 70):
				aDir(False)
				sidespeed = 50
			elif (xavg > 230):
				aDir(True)
				sidespeed = 50
			else:
				sidespeed = 0
		
		error = SET_DIST - currdist

		if error < 0:
			bDir(True)
			cDir(False)
		else:
			bDir(False)
			cDir(True)
		error = abs(error)
		
		if (error > 7):
			speed = error * kp
			if speed > 100:
				speed = 90
			elif speed < 0:
				speed = 0
		else:
			speed = 0
		print(speed)
	
		pwmA.ChangeDutyCycle(sidespeed)
		pwmB.ChangeDutyCycle(speed)
		pwmC.ChangeDutyCycle(speed)
		
		input_state = GPIO.input(ButtonSwitch)
		if input_state == False:
			print('FollowMe Mode ended Pressed')
			time.sleep(0.5)
			pwmA.ChangeDutyCycle(0)
			pwmB.ChangeDutyCycle(0)
			pwmC.ChangeDutyCycle(0)
			time.sleep(0.2)
			break
	

GPIO.cleanup()
#endpocketsphinx = subprocess.Popen("pkill pocketsphinx_co", shell=True)
#pvoice = subprocess.Popen("sudo python voice.py", shell=True)
