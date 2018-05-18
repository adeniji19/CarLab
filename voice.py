import subprocess
import os
import signal
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
from threading import Thread

# End process if previously running
endpocketsphinx = subprocess.Popen("sudo pkill pocketsphinx_co > /dev/null", shell=True)
print("Starting Voice Command...")

# Voice command function
# ===================================================
def execute(command):
	# Start voice command
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	output = ''

	for line in iter(p.stdout.readline,""):
		output = str(line)
		print('heard: ' + output)

		if ("LOKI" in output) and ("FOLLOW" in output):
			print ("Follow mode activated")
			p1 = subprocess.Popen("espeak \"follow mode activated\" -p 2 -g 5", shell=True)
			time.sleep(5)
			p1.kill()
			p.kill()
			pFollow = subprocess.Popen("sudo python pixy/build/libpixyusb_swig/followpix.py", shell=True)
			return
		elif ("LOKI" in output) and ("DEFENSE" in output):
			print ("Defense mode activated")
			p2 = subprocess.Popen("espeak \"defense mode activated\" -p 2 -g 5", shell=True)
			time.sleep(5)
			p2.kill()
			p.kill()
			pDefense = subprocess.Popen("python defense.py", shell=True)
			return
		elif ("LOKI" in output) and ("DANCE" in output):
			print ("Dance mode activated")
			pDance = subprocess.Popen("espeak \"it is time to dance\" -p 2 -g 5", shell=True)
			p3 = subprocess.Popen("mpg123 RobotVoice/party_song.mp3 2> /dev/null", shell=True)
			pDance = subprocess.Popen("python dance.py", shell=True)
			pDance.kill()
			p.kill()
			return
		elif ("LOKI" in output) and ("DRIVE" in output): #TRASH Mode
			print ("Trash mode activated")
			pTrashSound = subprocess.Popen("espeak \"place your garbage on my head\" -p 2 -g 5", shell=True)
			pTrash = subprocess.Popen("sudo python pixy/build/libpixyusb_swig/trash.py", shell=True)
			time.sleep(5)
			pTrash.kill()
			p.kill()
			pDefense = subprocess.Popen("python defense.py", shell=True)
			return
		elif ("LOKI" in output) and ("HELLO" in output): #JOKE Mode
			print ("joke mode activated")
			pDance = subprocess.Popen("espeak \"your face is a joke\" -p 2 -g 5", shell=True)
			p.kill()
			return
		elif ("LOKI" in output) and ("WORD" in output): #WEATHER Mode
			print ("weather mode activated")
			pDance = subprocess.Popen("espeak \"you are an engineer. you will never leave lab. do not worry about the weather.\" -p 2 -g 5", shell=True)
			p.kill()
			return

	p.wait()
	exitCode = p.returncode

	if (exitCode == 0):
		return output
	else:
		raise Exception("Error in Voice.py", exitCode)


# Call Voice Code #
# ===================================================
args = "pocketsphinx_continuous -inmic yes -adcdev plughw:1,0 -lm data/8398.lm -dict data/8398.dic 2> error.log"
# Stop all motors
pStop = subprocess.Popen("python stop.py", shell=True)
# Set volume
pVolume = subprocess.Popen("amixer set 'Master' 98%", shell=True)
# Startup voice
pStart = subprocess.Popen("espeak \"hello. I am loki. I am here to serve.\" -p 2", shell=True)
time.sleep(2)
pStop.kill()
pVolume.kill()
print("Motors stopped.")
execute(args)
print('end')
