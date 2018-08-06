################################################################################
#
# Bare Conductive Pi Cap
# ----------------------
#
# tts.py - touch triggered text-to-speech synthesis
#
# Written for Raspberry Pi.
#
# Bare Conductive code written by Szymon Kaliski and Tom Hartley.
#
# This work is licensed under a MIT license https://opensource.org/licenses/MIT
#
# Copyright (c) 2016, Bare Conductive
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#################################################################################

from subprocess import call
from time import sleep
import MPR121
from gpiozero import RGBLED

try:
  sensor = MPR121.begin()
except exception as e:
  print (e)
  sys.exit(1)

num_electrodes = 12

# this is the touch threshold - setting it low makes it more like a proximity trigger default value is 40 for touch
touch_threshold = 40

# this is the release threshold - must ALWAYS be smaller than the touch threshold default value is 20 for touch
release_threshold = 20

# set the thresholds
sensor.set_touch_threshold(touch_threshold)
sensor.set_release_threshold(release_threshold)

led = RGBLED(6, 5, 26, active_high=False)

# run espeak from shell
def speak(text):
  command = "espeak \"{text}\" --stdout | aplay > /dev/null 2>&1".format(text = text.replace("\n", " "))
  call(command, shell = True)

# load texts
texts = []
for i in range(num_electrodes):
  path = "texts/TEXT{0:03d}.txt".format(i)
  print ("loading file: " + path)

  text = open(path, 'r').read()
  texts.append(text)

running = True
while running:
  try:
    if sensor.touch_status_changed():
      sensor.update_touch_data()
      is_any_touch_registered = False

      # check if touch is registred to set the led status
      for i in range(num_electrodes):
        if sensor.is_new_touch(i) and not is_any_touch_registered:
          # play sound associated with that touch
          print ("speaking text: " + texts[i])
          speak(texts[i])
        if sensor.get_touch_data(i):
          is_any_touch_registered = True

      # light up red led if we have any touch registered currently
      if is_any_touch_registered:
        led.color = (1, 0, 0)
      else:
        led.color = (0, 0, 0)
    sleep(0.01)
  except KeyboardInterrupt:
    led.off()
    running = False
