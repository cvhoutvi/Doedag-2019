#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from datetime import date

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

getal = True

today = date.today()

naam = 'Doedag leerling'

blink_interval = 1 #Time interval in Seconds

try:
  
	print ('***********************')
	print ('*   Aansturing LEDs   *')
	print ('***********************\n')
	naam = input ('Wat is uw naam? ')
	naam = naam.title()		# Eerste letter van elk woord in hoofdletters
	print('\nDag ' + naam + ', welkom op de Doedag ' + str(today.year) + '.\n')
	
	try:
		aantal = int(input('Hoeveel keer moet ik knipperen (1 - 5) ? '.format(naam)))
		while aantal not in range (1,6):
			aantal = int(input('{}. Kies een getal vanaf 1 tot en met 5) ? '.format(naam)))
	except ValueError:
		print ('!!! {} dit is geen getal !!!'.format(naam.upper()))
		getal = False

	if getal:
		Leds = (8,10,12,16)
		for Led in Leds:
			GPIO.setup(Led, GPIO.OUT)
			GPIO.output(Led, False)


		# Blinker Loop
		for j in range (aantal):
			for Led in Leds:
				GPIO.output(Led, True)
			time.sleep(blink_interval)
			for Led in Leds:
				GPIO.output(Led, False)
			time.sleep(blink_interval)
		for j in range (aantal):
			for i in range (3,-1,-1):
				for Led in Leds:
					GPIO.output(Led, False)
				GPIO.output(Leds[i], True)
				time.sleep(0.15)
			for i in range (0,4,+1):
				for Led in Leds:
					GPIO.output(Led, False)
				GPIO.output(Leds[i], True)
				time.sleep(0.15)

except KeyboardInterrupt:
	print('\n\nOops! {} heeft het knipperen onderbroken.'.format(naam.upper()))

finally:
	GPIO.cleanup()
print("\nProgramma einde")
