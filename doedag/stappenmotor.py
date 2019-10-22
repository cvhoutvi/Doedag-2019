#!/usr/bin/env python3
#
# wave drive aansturing stappenmotor
#
#wave drive 1: 1 0 0 0
#wave drive 2: 0 1 0 0
#wave drive 3: 0 0 1 0
#wave drive 4: 0 0 0 1

import RPi.GPIO as GPIO
import time
from datetime import date

# USe RPi board notation (fysical pin numbers)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

today = date.today()

Yes_No = 		{
				'Yes' : ('ja', 'j', 'y', 'yes'),
				'No' : ('nee', 'neen' ,'n' , 'no')
				}

Rechts_Links = 	{
				'Rechts' : ('rechts', 'r', 'rechtsom', 're', 'rec', 'rech', 'recht'),
				'Links' : ('links', 'l', 'linksom', 'li', 'lin', 'link')
				}
				
Toeren_Graden = {
				'Tr' : ('Toeren', 't', 'tr'),
				'Gr' : ('Graden', 'g', 'gr')
				}
# pinnen
pin_blue = 8
pin_purple = 10
pin_yellow = 12
pin_orange = 16

delay = 0.002

gear = 63.65				# verhouding van de vertragingsbox
oneFullStep = 11.25/gear	# motor heeft 32 posities ==> 360° / 32 = 11,25° per stap

#    GPIO.setup(pin, GPIO.OUT)

GPIO.setup(pin_blue, GPIO.OUT)
GPIO.setup(pin_purple, GPIO.OUT)
GPIO.setup(pin_yellow, GPIO.OUT)
GPIO.setup(pin_orange, GPIO.OUT)
class InputError (Exception):
	def __init__(self, data):    
		self.data = data
	def __str__(self):
		return repr(self.data)
		
def question (Antwoord, AntwoordLijst):		# Deze functie zoekt of een Antwoord in een gestructureerde Antwoordlijst voorkomt.
    ReturnValue="0"
    for index in list(AntwoordLijst):
         for MogelijkAntwoord in AntwoordLijst[index]:
            if (Antwoord.lower() == MogelijkAntwoord.lower()):
                ReturnValue = index
    return(ReturnValue)
	
# functie om pin state te veranderen
def setstep(w1,w2,w3,w4) :
    GPIO.output(pin_blue, w1)
    GPIO.output(pin_purple, w2)
    GPIO.output(pin_yellow, w3)
    GPIO.output(pin_orange, w4)

def RotateCounterClockWise (graden) :
	
	for i in range (int(graden/oneFullStep/4)) :		# gedeeld door 4 omdat we vier stappen definiëren in onderstaand code
		#wave drive
		setstep(1,0,0,0)
		time.sleep(delay)
		setstep(0,1,0,0)
		time.sleep(delay)
		setstep(0,0,1,0)
		time.sleep(delay)
		setstep(0,0,0,1)
		time.sleep(delay)

def RotateClockWise (graden) :
	
	for i in range (int(graden/oneFullStep/4)) :		# gedeeld door 4 omdat we vier stappen definiëren in onderstaand code
		#wave drive
		setstep(0,0,0,1)
		time.sleep(delay)
		setstep(0,0,1,0)
		time.sleep(delay)
		setstep(0,1,0,0)
		time.sleep(delay)
		setstep(1,0,0,0)
		time.sleep(delay)		
		
setstep(0,0,0,0)	# reset alle pinnen
getError = False
naam = 'Doedag leerling'

try:
	print ('*******************************')
	print ('*   Aansturing stappenmotor   *')
	print ('*******************************\n')
	
	naam = input ('Wat is uw naam? ')
	naam = naam.title()		# Eerste letter van elk woord in hoofdletters
	
	print('\nDag ' + naam + ', welkom op de Doedag ' + str(today.year) + '.')
	print('\nDit programma kan met toeren of met graden werken.')
	print('Als je toeren kiest, geef je nadien het aantal omwentelingen in.')
	print('Als je graden kiest, moet je het aantal graden ingeven.')
	
	tr_gr = question(input('Toeren of graden ? '),Toeren_Graden)
	while (tr_gr) == "0":
			tr_gr = question(input('Foutief antwoord. Toeren of graden ? '),Toeren_Graden)
	try:
		if tr_gr == 'Tr':
			aantal = int(input('Hoeveel toeren moet de motor ronddraaien (1 - 5) ? '.format(naam)))
			while aantal not in range (1,6):
				aantal = int(input('{}. Kies een getal vanaf 1 tot en met 5 ? '.format(naam)))
		elif tr_gr == 'Gr':
			aantal = int(input('Hoeveel graden moet de motor draaien (10 - 360) ? '.format(naam)))
			while aantal not in range (10,361):
				aantal = int(input('{}. Kies een getal vanaf 10 tot en met 360 ? '.format(naam)))
		else:
			raise InputError('Geen graden of toeren gegeven')
			
		richt = question(input('Draait de motor rechtsom of linksom ? '),Rechts_Links)
		while (richt) == "0":
			richt = question(input('Foutief antwoord. Draait de motor rechtsom of linksom ? '),Rechts_Links)
				
	except ValueError:
		print ('!!! {} dit is geen getal !!!'.format(naam.upper()))
		getError = True
	except InputError as error:
		print ('Received Error:', error.data)
		getError = True
		
	if not getError:
		if tr_gr == 'Tr':
			aantalGraden = 360 * aantal
		elif tr_gr == 'Gr':
			aantalGraden = aantal
		else:
			aantalGraden = 0

		if richt == 'Rechts':
			RotateClockWise(aantalGraden)
		elif richt == 'Links':
			RotateCounterClockWise(aantalGraden)
		else:
			print('Error: Motor weet geen richting')
	
except KeyboardInterrupt:
  print('\n\nOops! {} heeft het draaien onderbroken.'.format(naam.upper()))
  # Release Resources
finally:
  setstep(0,0,0,0)	# reset alle pinnen
  GPIO.cleanup()
print("\nProgramma einde")
