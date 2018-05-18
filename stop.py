import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

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

# ****************************************************
# Forward motor movement
# ****************************************************
def forward():
	# set directions
	aDir(False)
	bDir(True)
	cDir(True)
	# start motors
	pwmA.start(A)
	pwmB.start(B)
	pwmC.start(C)

	# Ramp up the appropriate motors
	for i in range(5):
		pwmA.ChangeDutyCycle(50)
		pwmB.ChangeDutyCycle(0)
		pwmC.ChangeDutyCycle(50)
		time.sleep(1)
	allStop()

# ****************************************************
# Backward motor movement
# ****************************************************
def backward():
	# set directions
	aDir(True)
	bDir(True)
	cDir(False)
	# start motors
	pwmA.start(A)
	pwmB.start(B)
	pwmC.start(C)

	# Ramp up the appropriate motors
	for i in range(5):
		pwmA.ChangeDutyCycle(75)
		pwmB.ChangeDutyCycle(0)
		pwmC.ChangeDutyCycle(75)
		time.sleep(1)
	allStop()

# ****************************************************
# Right table movement
# ****************************************************
def right():
	# set directions
	aDir(False)
	bDir(True)
	cDir(True)
	# start motors
	pwmA.start(A)
	pwmB.start(B)
	pwmC.start(C)

	# Ramp up the appropriate motors
	for i in range(5):
		pwmA.ChangeDutyCycle(75)
		pwmB.ChangeDutyCycle(75 * sideStep)
		pwmC.ChangeDutyCycle(75 * sideStep)
		time.sleep(1)
	allStop()
	
# ****************************************************
# Right table movement
# ****************************************************
def left():
	# set directions
	aDir(True)
	bDir(False)
	cDir(False)
	# start motors
	pwmA.start(A)
	pwmB.start(B)
	pwmC.start(C)

	# Ramp up the appropriate motors
	for i in range(5):
		pwmA.ChangeDutyCycle(75)
		pwmB.ChangeDutyCycle(75 * sideStep)
		pwmC.ChangeDutyCycle(75 * sideStep)
		time.sleep(1)
	allStop()

# ****************************************************
# Spin motor movement
# Clockwise for true; Counter for false
# ****************************************************
def spin(dir):
	# set directions
	aDir(dir)
	bDir(dir)
	cDir(dir)
	# start motors
	pwmA.start(A)
	pwmB.start(B)
	pwmC.start(C)

	# Ramp up the appropriate motors
	for i in range(10):
		pwmA.ChangeDutyCycle(50)
		pwmB.ChangeDutyCycle(50)
		pwmC.ChangeDutyCycle(50)
		time.sleep(1)
	allStop()

# ****************************************************
# Initial setup function, called once
# RETURNS: none
# ****************************************************
GPIO.setwarnings(False)

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

# set default directions
aDir(True)
bDir(True)
cDir(True)

# Command all motors to stop
allStop()

#spin(True)
#time.sleep(2)
#spin(False)
#time.sleep(2)
#forward()
#time.sleep(2)
#backward()
#time.sleep(2)
#right()
#time.sleep(2)
#left()
print("stopped")
GPIO.cleanup()
