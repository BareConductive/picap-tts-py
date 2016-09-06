################################################################################
#
#  Bare Conductive Pi Cap
#  ----------------------
#
#  tts.py - touch triggered text-to-speech synthesis
#
#  Written for Raspberry Pi.
#
#  Bare Conductive code written by Szymon Kaliski.
#
#  This work is licensed under a Creative Commons Attribution-ShareAlike 3.0
#  Unported License (CC BY-SA 3.0) http://creativecommons.org/licenses/by-sa/3.0/
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.
#
#################################################################################

from subprocess import call
from time import sleep
import signal, sys, MPR121
import RPi.GPIO as GPIO

try:
  sensor = MPR121.begin()
except exception as e:
  print e
  sys.exit(1)

num_electrodes = 12

# handle ctrl+c gracefully
def signal_handler(signal, frame):
  light_rgb(0, 0, 0)
  sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# set up led
red_led_pin = 6
green_led_pin = 5
blue_led_pin = 26

def light_rgb(r, g, b):
  # we are inverting the values, because the led is active low
  # low - on
  # high - off
  GPIO.output(red_led_pin, not r)
  GPIO.output(green_led_pin, not g)
  GPIO.output(blue_led_pin, not b)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red_led_pin, GPIO.OUT)
GPIO.setup(green_led_pin, GPIO.OUT)
GPIO.setup(blue_led_pin, GPIO.OUT)

light_rgb(0, 0, 0)

# run espeak from shell
def speak(text):
  command = "espeak \"{text}\" --stdout | aplay > /dev/null 2>&1".format(text = text.replace("\n", " "))
  call(command, shell = True)

# load texts
texts = []
for i in range(num_electrodes):
  path = "texts/TEXT{0:03d}.txt".format(i)
  print "loading file: " + path

  text = open(path, 'r').read()
  texts.append(text)

while True:
  if sensor.touch_status_changed():
    sensor.update_touch_data()
    is_any_touch_registered = False

    # check if touch is registred to set the led status
    for i in range(num_electrodes):
      if sensor.is_new_touch(i) and not is_any_touch_registered:
        # play sound associated with that touch
        print "speaking text: " + texts[i]
        speak(texts[i])
      if sensor.get_touch_data(i):
        is_any_touch_registered = True

    # light up red led if we have any touch registered currently
    if is_any_touch_registered:
      light_rgb(1, 0, 0)
    else:
      light_rgb(0, 0, 0)

  # sleep a bit
  sleep(0.01)
