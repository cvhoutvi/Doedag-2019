import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)
GPIO.setmode(GPIO.BOARD)

# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   8 : {'name' : 'Living', 'state' : GPIO.LOW},
   10 : {'name' : 'Keuken', 'state' : GPIO.LOW},
   12 : {'name' : 'WC', 'state' : GPIO.LOW},
   16 : {'name' : 'Gang', 'state' : GPIO.LOW}
   }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'voornaam' : voornaam,
	  'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('led.html', **templateData)

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      GPIO.output(changePin, GPIO.HIGH)
      # Save the status message to be passed into the template:
      message = "Licht " + deviceName + " aan."
   if action == "off":
      GPIO.output(changePin, GPIO.LOW)
      message = "Licht " + deviceName + " uit."
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      GPIO.output(changePin, not GPIO.input(changePin))
      message = "Toggled " + deviceName + "."

   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'voornaam' : voornaam,
      'message' : message,
      'pins' : pins
   }

   return render_template('led.html', **templateData)

try:
   if __name__ == "__main__":
      voornaam = input ("Wat is uw voornaam? ")
      app.run(host='0.0.0.0', port=80, debug=False)
except KeyboardInterrupt:
   print("\nyou pressed ctrl-C")
finally:
   GPIO.cleanup()
   print("\nGPIO cleanup is done")
