import time
import sys
import subprocess
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

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

purple = 32
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

# Globals
sideStep = 0.33; # Limiting factor to ensure direct side to side movement

pVolume = subprocess.Popen("amixer set 'Master' 98% > /dev/null", shell=True)
time.sleep(.1)
pVolume.kill()
psp = subprocess.Popen("espeak \"defense mode activated\" -p 2 -g 5", shell=True)
time.sleep(.1)
psp.kill()
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

def allPause():
	pwmA.ChangeDutyCycle(0)
	pwmB.ChangeDutyCycle(0)
	pwmC.ChangeDutyCycle(0)
	time.sleep(0.2)

TrigU1 = 11
EchoU1 = 21
TrigU2 = 37
EchoU2 = 35
TrigU3 = 5
EchoU3 = 3
TrigU4 = 15
EchoU4 = 13

GPIO.setwarnings(False)

GPIO.setup(TrigU1, GPIO.OUT)
GPIO.output(TrigU1, False)
GPIO.setup(TrigU2, GPIO.OUT)
GPIO.output(TrigU2, False)
GPIO.setup(TrigU3, GPIO.OUT)
GPIO.output(TrigU3, False)
GPIO.setup(TrigU4, GPIO.OUT)
GPIO.output(TrigU4, False)

GPIO.setup(EchoU1, GPIO.IN)
GPIO.setup(EchoU2, GPIO.IN)
GPIO.setup(EchoU3, GPIO.IN)
GPIO.setup(EchoU4, GPIO.IN)

time.sleep(0.1)

print("Starting defense mode...")
print("Starting measurement...")

# set directions
aDir(True)
bDir(True)
cDir(True)
# start motors
pwmA.start(A)
pwmB.start(B)
pwmC.start(C)

spinSpeed = 30
speed = 50
sidespeed = 0

pwmA.ChangeDutyCycle(spinSpeed)
pwmB.ChangeDutyCycle(spinSpeed)
pwmC.ChangeDutyCycle(spinSpeed)

foundLocation = 6

while True:
	time.sleep(0.0001)
	GPIO.output(TrigU1, True)
	time.sleep(0.0001)
	GPIO.output(TrigU1, False)

	while GPIO.input(EchoU1) == 0:
		pass
	start = time.time()

	while GPIO.input(EchoU1) == 1:
		pass
	stop = time.time()
	
	dist1 = (stop-start) * 17150
	#print(dist1)
	if (dist1 > 30) and (dist1 < 150):
		print("FRONT - " + str(dist1))
		foundLocation = 0
		break
	
	time.sleep(0.0001)
	GPIO.output(TrigU2, True)
	time.sleep(0.0001)
	GPIO.output(TrigU2, False)

	while GPIO.input(EchoU2) == 0:
		pass
	start = time.time()

	while GPIO.input(EchoU2) == 1:
		pass
	stop = time.time()
	
	dist2 = (stop-start) * 17150
	if (dist2 > 30) and (dist2 < 150):
		print("RIGHT - " + str(dist2))
		foundLocation = -1
		break
		
		
	time.sleep(0.0001)
	GPIO.output(TrigU4, True)
	time.sleep(0.0001)
	GPIO.output(TrigU4, False)

	while GPIO.input(EchoU4) == 0:
		pass
	start = time.time()

	while GPIO.input(EchoU4) == 1:
		pass
	stop = time.time()
	
	dist4 = (stop-start) * 17150
	if (dist4 > 30) and (dist4 < 150):
		print("LEFT - " + str(dist4))
		foundLocation = 1
		break


#open laser trap door
GPIO.output(purple, True)
#GPIO.output(white, True)
print("changed")
	
allPause()


spinSpeed = 90

pwmA.ChangeDutyCycle(spinSpeed)
pwmB.ChangeDutyCycle(spinSpeed)
pwmC.ChangeDutyCycle(spinSpeed)

pAttack = subprocess.Popen("espeak \"prepare to die\" -p 2", shell=True)
time.sleep(3)
pPewPew = subprocess.Popen("mpg123 RobotVoice/laser.mp3 2> /dev/null", shell=True)
time.sleep(6)
pAttack.kill()
pPewPew.kill()
allStop()
time.sleep(2)



GPIO.cleanup()
#endpocketsphinx = subprocess.Popen("pkill pocketsphinx_co", shell=True)
#pvoice = subprocess.Popen("sudo python voice.py", shell=True)